import math

from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import Truncator

from markdown import markdown


class SportMeet(models.Model):
    name = models.CharField("项目名称", max_length=30, unique=True)
    description = models.CharField("项目描述", max_length=100)
    numbers_of_sport_meet = models.IntegerField("参加此项目的人数", default=0)
    sport_meet_group = models.CharField("项目所属分组", max_length=30, default=0)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Announcement(models.Model):
    name = models.CharField("公告标题", max_length=30, unique=True)
    description = models.CharField("公告类型", max_length=100)
    numbers_of_sport_meet = models.CharField("公告内容", max_length=150, default=0)
    sport_meet_group = models.CharField("上传部门", max_length=30, default=0)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Classes(models.Model):
    classes_grade = models.CharField('年级', max_length=32, null=True)
    classes_class = models.CharField('班级', max_length=64, null=True)

    def __str__(self):
        return self.classes_class

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


academy = (
    ('school', '清华大学'),
    ('Mines', '矿业学院'),
    ('Law', '法学院'),
    ('Art_Design', '美术学院'),
    ('Economics', '经济学院'),
    ('Management', '管理学院'),
    ('Computer_Science', '计算机科学学院')
)


class SUser(models.Model):
    """
    用户表
    """
    user_id = models.AutoField('用户编号', primary_key=True)
    user_nick = models.CharField('用户名（昵称）', max_length=32, unique=True)
    user_pwd = models.CharField(max_length=128)
    user_name = models.CharField('姓名', max_length=32)
    user_phonenumber = models.CharField('手机号', max_length=32, blank=True, null=True)
    role_type = (('manager', '管理员'), ('user', '运动员'))
    user_role = models.CharField('身份', choices=role_type, max_length=16, default='manager', blank=True, null=True)
    sex_type = (('male', '男'), ('female', '女'))
    user_sex = models.CharField('性别', choices=sex_type, max_length=32, blank=True, null=True)
    user_academy = models.CharField('学院', max_length=32, choices=academy, null=True)
    classes_id = models.ForeignKey('Classes', on_delete=models.CASCADE, verbose_name='班级', default=1)


class Application(models.Model):
    """
    申请表
    """
    status_type = (('unapprove', '未通过'), ('approve', '通过'), ('unreview', '未审核'))
    app_status = models.CharField('审核状态', max_length=20, choices=status_type, default='unreview', null=True)
    sport_id = models.ForeignKey('SportMeet', verbose_name='运动项目', null=True)
    user_id = models.ForeignKey('SUser', verbose_name='用户')


class Score(models.Model):
    """
    成绩表
    """
    user_id = models.ForeignKey('SUser', verbose_name='用户')
    sport_id = models.ForeignKey('SportMeet', verbose_name='运动项目')
    score = models.IntegerField('分数', default=0)


class Notice(models.Model):
    """
    公告表
    """
    notice_item = models.CharField('公告标题', max_length=64)
    news_type = (('picture_news', '图片新闻'), ('video_news', '视频新闻'))
    notice_type = models.CharField('新闻类型', max_length=32, choices=news_type)
    notice_picture_content = models.ImageField('图片新闻公告内容', upload_to='p_content')
    notice_video_content = models.FileField('视频新闻公告内容', upload_to='v_content')
    notice_academy = models.CharField('学院', max_length=32, choices=academy, null=True)


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

# from django.db import models
#
# # Create your models here.
#
#
# academy = (
#     ('school', '清华大学'),
#     ('Mines', '矿业学院'),
#     ('Law', '法学院'),
#     ('Art_Design', '美术学院'),
#     ('Economics', '经济学院'),
#     ('Management', '管理学院'),
#     ('Computer_Science', '计算机科学学院')
# )
#
#
# class Classes(models.Model):
#     """
#     班级表
#     """
#     classes_grade = models.CharField('年级', max_length=32, null=True)
#     classes_class = models.CharField('班级', max_length=64, null=True)
#
#
# class Sport(models.Model):
#     """
#     运动项目表
#     """
#     sport_name = models.CharField('项目名', max_length=64)
#     sport_limit = models.IntegerField('人数限定', default=0)
#
#
# class SUser(models.Model):
#     """
#     用户表
#     """
#     user_id = models.AutoField('用户编号', primary_key=True)
#     user_nick = models.CharField('用户名（昵称）', max_length=32, unique=True)
#     user_pwd = models.CharField(max_length=128)
#     user_name = models.CharField('姓名', max_length=32)
#     user_phonenumber = models.CharField('手机号', max_length=32, blank=True, null=True)
#     role_type = (('manager', '管理员'), ('user', '用户'))
#     user_role = models.CharField('身份', choices=role_type, max_length=16, default='manager', blank=True, null=True)
#     sex_type = (('male', '男'), ('female', '女'))
#     user_sex = models.CharField('性别', choices=sex_type, max_length=32, blank=True, null=True)
#     user_academy = models.CharField('学院', choices=academy, null=True)
#     classes_id = models.ForeignKey('Classes', on_delete=models.CASCADE, verbose_name='班级')
#
#
# class Application(models.Model):
#     """
#     申请表
#     """
#     status_type = (('unapprove', '未通过'), ('approve', '通过'), ('unreview', '未审核'))
#     app_status = models.CharField('审核状态', choices=status_type, default='unreview', null=True)
#     sport_id = models.ForeignKey('Sport', verbose_name='运动项目', null=True)
#     user_id = models.ForeignKey('boards.models.SUser', verbose_name='用户')
#
#
# class Score(models.Model):
#     """
#     成绩表
#     """
#     user_id = models.ForeignKey('boards.models.SUser', verbose_name='用户')
#     sport_id = models.ForeignKey('Sport', verbose_name='运动项目')
#     score = models.IntegerField('分数', default=0)
#
#
# class Notice(models.Model):
#     """
#     公告表
#     """
#     notice_item = models.CharField('公告标题', max_length=64)
#     news_type = (('picture_news', '图片新闻'), ('video_news', '视频新闻'))
#     notice_type = models.CharField('新闻类型', choices=news_type)
#     notice_picture_content = models.ImageField('图片新闻公告内容', upload_to='p_content')
#     notice_video_content = models.FileField('视频新闻公告内容', upload_to='v_content')
#     notice_academy = models.CharField('学院', choices=academy, null=True)
