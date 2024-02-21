from datetime import datetime
from tabnanny import verbose
from tkinter import CASCADE
from django.db import models
from myApp.models import Job_type, getjob
from django.utils import timezone
from mysql_member.models import Member
from dirtyfields import DirtyFieldsMixin
# Create your models here.

class Like(DirtyFieldsMixin,models.Model):
    like_user_name = models.ForeignKey(Member,related_name ='user_name',on_delete=models.CASCADE,verbose_name='帳號')
    like_jobid =  models.ForeignKey(getjob,related_name ='job_id',on_delete=models.CASCADE,default="",verbose_name='工作id')
    like_user_skill = models.CharField(max_length=200,null=False,default="",verbose_name='用戶技能')
    like_certificate = models.CharField(max_length=500,null=True)
    like_type = models.CharField(max_length=200,null=False,default="like",verbose_name='工作類型')
    like_date = models.DateField(max_length=300,verbose_name='添加時間',default=timezone.now)
    class Meta:
        db_table = 'Like'
        verbose_name = '用戶最愛管理'
        verbose_name_plural = '用戶最愛管理'

class Recommend(DirtyFieldsMixin,models.Model):
    recom_user_name = models.OneToOneField(Member,on_delete=models.CASCADE,verbose_name='帳號')
    recom_open = models.BooleanField(null=False,default=False,verbose_name='是否開啟推送')
    recom_job_type = models.ForeignKey(Job_type,on_delete=models.CASCADE,null=True,verbose_name='推送工作類型',db_column='recom_job_type')
    recom_skill = models.CharField(max_length=300,null=False,verbose_name='推送篩選技能',default="")
    recom_fraction = models.CharField(max_length=300,null=True,verbose_name='推送篩選標準',default="max")
    recom_count = models.CharField(max_length=300,null=False,default="0",verbose_name='推送數量')
    recom_local = models.CharField(max_length=300,null=True)
    recom_Experience = models.IntegerField(null=True)
    recom_cer_boo = models.BooleanField(null=False,default=False)
    recom_cer_fraction = models.CharField(max_length=300,null=True,verbose_name='推送篩選標準',default="max")
    recom_certificate =models.CharField(max_length=500,null=True)
    recom_email_open = models.BooleanField(null=False,default=False,verbose_name='是否開啟Email推送')
    recom_line_bot = models.BooleanField(null=False,default=False,verbose_name='是否開啟line-bot推送')
    class Meta:
        db_table = 'Recommend'
        verbose_name='推送管理'
        verbose_name_plural = '推送管理'
class Recommend_log(DirtyFieldsMixin,models.Model):
    relog_id = models.AutoField(verbose_name='ID',primary_key=True)
    relog_user_name = models.ForeignKey(Member,on_delete=models.CASCADE,verbose_name='推送帳號')
    relog_datetime =models.DateTimeField(verbose_name='推送時間',default=timezone.now)
    relog_count = models.IntegerField(verbose_name='推送數量')
    relog_state = models.BooleanField(null=False,default=True,verbose_name='狀態')
    relog_content = models.CharField(max_length=3000,null=True,verbose_name='詳細內容')
    class Meta:
        db_table = 'Recommend_log'
        verbose_name='推送日誌'
        verbose_name_plural = '推送日誌'
class Notice(DirtyFieldsMixin,models.Model):
    Notice_id =models.AutoField(null=False,verbose_name='ID',primary_key=True)
    Notice_content = models.CharField(max_length=3000,null=False,verbose_name='通知內容')
    Notice_title = models.CharField(max_length=300,null=False,verbose_name='通知標題',default='推送通知')
    Notice_user = models.ForeignKey(Member,on_delete=models.CASCADE,verbose_name='通知帳號')
    Notice_date = models.DateField(default=timezone.now,verbose_name='通知日期')
    Notice_look = models.BooleanField(verbose_name='是否查看')
    class Meta:
        db_table = 'Notic'
        verbose_name='通知中心'
        verbose_name_plural = '通知中心'
class Opinion(DirtyFieldsMixin,models.Model):
    opinion_id = models.AutoField(null=False,verbose_name='ID',primary_key=True)
    opinion_date =models.DateTimeField(verbose_name='時間',default=timezone.now)
    opinion_user_name = models.ForeignKey(Member,on_delete=models.CASCADE,verbose_name='帳號')
    opinion_type = models.CharField(max_length=300,null=False,verbose_name='意見類型')
    opinion_content = models.CharField(max_length=5000,verbose_name='意見內容')
    opinion_response = models.OneToOneField(Notice,null=True,on_delete=models.CASCADE,verbose_name='回覆狀態')
    opinion_img = models.ImageField(upload_to="uploads/",null=True,blank=True)
    class Meta:
        db_table = 'Opinion'
        verbose_name='意見箱'
        verbose_name_plural = '意見箱'