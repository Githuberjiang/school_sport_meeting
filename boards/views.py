from django.db.models import Count
from django.db import models
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse

from .forms import NewTopicForm, PostForm
from .models import SportMeet, Post, Topic, Notice, SportScores, Application, StudentUser, User


sport_limit_dict = {

}

class BoardListView(ListView):
    model = Notice
    context_object_name = 'boards'
    template_name = 'home.html'


class Show(ListView):
    model = SportMeet
    context_object_name = 'sports'
    template_name = 'show.html'


class ShowScores(ListView):
    model = SportScores
    context_object_name = "scores"
    template_name = "scores.html"


def apply(request):
    global sport_limit_dict
    sport_name = SportMeet.objects.all().values_list()
    print(sport_name)
    if request.method == "POST":

        form_data = request.POST
        studen_name = form_data.get("student_name")
        spo_name = form_data.get("sport_name")
        spo_obj = SportMeet.objects.filter(sport_name=spo_name)
        stu_obj = StudentUser.objects.filter(student_true_name=studen_name)
        # spo_limit = SportMeet.objects.filter(sport_limit_people=)
        if spo_obj and stu_obj:
            if Application.objects.filter(sport_id=spo_obj[0], user_id=stu_obj[0]):
                err = "报名信息已存在"
                return render(request, 'apply.html', {"err": err})
            Application.objects.create(sport_id=spo_obj[0], user_id=stu_obj[0])
            status = Application.objects.filter(user_id=stu_obj)[0].app_status
            print(status)
            return render(request, "apply.html", {"status": "报名状态："+status})
        else:
            err = "填写信息有误，请核实"
            return render(request, 'apply.html', {"err": err})
    else:
        user = request.path_info.split("/")[2]
        user_obj = User.objects.filter(username=user)[0]
        user_true_name = user_obj.student_user.first().student_true_name
        # user_ture_name = User.objects.filter(first_name=user_obj).values("first_name")
        sports = SportMeet.objects.all()

        return render(request, 'apply.html', {"user_true_name": user_true_name, "sports": sports})


def status(request):
    print(request.GET)
    user = request.path_info.split("/")[2]
    print(user)
    # status_ = Application.objects.filter(user_id=user)
    user_obj = User.objects.filter(username=user)
    status = Application.objects.filter(app_status=user_obj)
    # print(user_obj[0].first_name, status)
    return render(request, 'status.html')



def search(request):
    q = request.POST.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入正确的关键词'
        return render(request, 'search.html', {'error_msg': error_msg})

    search_list = SportMeet.objects.filter(sport_name__istartswith=q)
    return render(request, 'search.html', {'error_msg': error_msg,
                                           'search_list': search_list})


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(SportMeet, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
def new_topic(request, pk):
    board = get_object_or_404(SportMeet, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)
