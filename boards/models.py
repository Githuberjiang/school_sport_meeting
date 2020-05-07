import math

from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import Truncator

from markdown import markdown


class StudentUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='student_user')
    student_name = models.CharField("用户名称", max_length=16)
    student_password = models.CharField("密码", max_length=16)
    student_college = models.CharField("学院", max_length=16)
    student_class = models.CharField("班级", max_length=16)
    student_true_name = models.CharField("姓名", max_length=16)
    sex_type = (('男', '男'), ('女', '女'))
    phone_number = models.IntegerField("电话", default=1)


class Notice(models.Model):
    notice_title = models.CharField("公告标题", max_length=16, default="")
    notice_type = models.CharField("公告类型", max_length=16, default="图片新闻", choices=(('图片新闻', '图片新闻'), ('视频新闻', '视频新闻')))
    notice_content = models.CharField("内容描述", max_length=140,default="")
    update_group = models.CharField("上传单位", max_length=16, default='')
    update_user = models.CharField("作者", max_length=16, default='')
    update_date = models.DateField("日期", auto_now=True)


class SportMeet(models.Model):
    sport_name = models.CharField("项目名称", max_length=16, default="")
    sport_limit_people = models.IntegerField("限定人数", default=0)
    sport_group = models.CharField("比赛分组", max_length=16, default="")
    sport_address = models.CharField("比赛地点", max_length=32, default="")
    sport_date = models.DateField("比赛时间", auto_now=True)


class SportScores(models.Model):
    scores_college = models.CharField("学院", max_length=16)
    student_class = models.CharField("班级", max_length=16)
    student_name = models.CharField("姓名", max_length=16)
    winner_sport= models.CharField("获奖项目", max_length=16)
    apply_date = models.DateField("参赛日期", auto_now=True)
    sport_rank = models.CharField("名次等级", max_length=16)


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(SportMeet, related_name='topics')
    starter = models.ForeignKey(User, related_name='topics')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts')
    updated_by = models.ForeignKey(User, null=True, related_name='+')

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
