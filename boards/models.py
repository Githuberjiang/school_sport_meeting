import math

from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import Truncator

from markdown import markdown



class StudentUser(models.Model):
    class Meta:
        verbose_name = "学生用户"

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='student_user')
    student_name = models.CharField("用户名称", max_length=16)
    student_password = models.CharField("密码", max_length=16)
    student_college = models.CharField("学院", max_length=16)
    student_class = models.CharField("班级", max_length=16)
    # student_true_name = models.CharField("姓名", max_length=16)
    sex_type = (('男', '男'), ('女', '女'))
    phone_number = models.CharField("电话",max_length=11, default=13345678889)

    def __str__(self):
        return self.student_true_name


class Notice(models.Model):
    class Meta:
        verbose_name = "公告信息"

    notice_title = models.CharField("公告标题", max_length=16, default="")
    notice_type = models.CharField("公告类型", max_length=16, default="图片新闻", choices=(('图片新闻', '图片新闻'), ('视频新闻', '视频新闻')))
    notice_content = models.CharField("内容描述", max_length=140, default="")
    notice_video_content = models.FileField('上传公告文件', upload_to='static')
    update_group = models.CharField("上传单位", max_length=16, default='')
    update_user = models.CharField("作者", max_length=16, default='')
    update_date = models.DateField("日期", auto_now=True)

    def __str__(self):
        return self.notice_title


class SportMeet(models.Model):
    class Meta:
        verbose_name = "运动会项目"

    sport_name = models.CharField("项目名称", max_length=16, default="")
    sport_limit_people = models.IntegerField("限定人数", default=0)
    sport_group = models.CharField("比赛分组", max_length=16, default="")
    sport_address = models.CharField("比赛地点", max_length=32, default="")
    sport_date = models.DateTimeField("比赛时间", default=None)
    sport_session = models.CharField("比赛场次", max_length=16, default="")

    def __str__(self):
        return self.sport_name


class SportScores(models.Model):
    class Meta:
        verbose_name = "运动会成绩"

    scores_college = models.CharField("学院", max_length=16)
    student_class = models.CharField("班级", max_length=16)
    student_name = models.CharField("姓名", max_length=16)
    winner_sport = models.CharField("获奖项目", max_length=16)
    apply_date = models.DateField("参赛日期", auto_now=True)
    sport_rank = models.CharField("名次等级", max_length=16)

    def __str__(self):
        return self.student_name


class Application(models.Model):
    class Meta:
        verbose_name = "报名审核"

    status_type = (('未通过', '未通过'), ('通过', '通过'), ('未审核', '未审核'))
    app_status = models.CharField('审核状态', choices=status_type, max_length=16, default='未审核', null=True)
    # apply_number = models.ForeignKey(SportMeet, verbose_name='限定人数', null=True)
    sport_id = models.ForeignKey(SportMeet, verbose_name='运动项目', null=True)
    user_id = models.ForeignKey(StudentUser, verbose_name='用户', null=True)

    def __str__(self):
        return self.app_status


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
