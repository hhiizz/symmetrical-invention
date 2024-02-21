import datetime
from email.policy import default
from tabnanny import verbose
from turtle import update
from dirtyfields import DirtyFieldsMixin
from django.db import models
from django.utils import timezone
from myApp.models import getjob

# Create your models here.
class Member(DirtyFieldsMixin,models.Model):
    user_id = models.IntegerField(verbose_name='ID',unique=True)
    username = models.CharField(max_length=100,default=None,primary_key=True,verbose_name='帳照', db_collation='utf8mb4_0900_as_cs')
    Email = models.EmailField(unique=True,verbose_name='Email',null=False,default='xxxxx@.com', db_collation='utf8mb4_0900_as_cs')
    password = models.CharField(max_length=100,default=None,verbose_name='密碼', db_collation='utf8mb4_0900_as_cs')
    datetime = models.DateField(default=timezone.now,verbose_name='創建日期')
    permissions  = models.BooleanField(default=False,verbose_name='權限')
    last_login = models.DateField(default=timezone.now,verbose_name='上次登入日期',null=False)
    line_user_id = models.CharField(max_length=300,unique=True,null=True,verbose_name="line_id",db_collation='utf8mb4_0900_as_cs')
    class Meta:
        db_table = 'member'
        verbose_name = '用戶管理'
        verbose_name_plural='用戶管理'
        
class Popular_job(DirtyFieldsMixin,models.Model):
    popular_jobid = models.ForeignKey(getjob,on_delete=models.CASCADE,null=True,verbose_name='工作id',db_column='popular_jobid')
    popular_job_user = models.ForeignKey(Member,on_delete=models.CASCADE,null=True,verbose_name='使用者',db_column='popular_job_user')
    class Meta:
        db_table = 'Popular_job'
        verbose_name = "工作歡迎度"
        verbose_name_plural = "工作歡迎度"


# 2.刪除操作
# 如果我們要刪除一個模型類該怎樣做呢？其實順序也是跟我們創建一個模型類是一樣的：

# 首先刪除，模型類的代碼
# 然後刪除，migrations文件夾下面對應的操作記錄文件
# 然後刪除，django_migrations表中對應的生成記錄
# 最後刪除，數據庫中的數據表
# 以上才是刪除一個模型類的正確流程。
