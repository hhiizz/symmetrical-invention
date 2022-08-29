import datetime
from email.policy import default
from turtle import update
from django.db import models
from django.utils import timezone
from myApp.models import getjob,getjob_firmware,getjob_hardware

from myApp.models import getjob,getjob_firmware,getjob_hardware
# Create your models here.
class Member(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=100,default=None,primary_key=True)
    password = models.CharField(max_length=100,default=None)
    datetime = models.DateField(default=timezone.now)
    class Meta:
        db_table = 'member'


# class Like(models.Model):
#     username = models.CharField(max_length=100,default=None)

# 2.刪除操作
# 如果我們要刪除一個模型類該怎樣做呢？其實順序也是跟我們創建一個模型類是一樣的：

# 首先刪除，模型類的代碼
# 然後刪除，migrations文件夾下面對應的操作記錄文件
# 然後刪除，django_migrations表中對應的生成記錄
# 最後刪除，數據庫中的數據表
# 以上才是刪除一個模型類的正確流程。
