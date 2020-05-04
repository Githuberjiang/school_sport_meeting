from django.db import models

# Create your models here.

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
