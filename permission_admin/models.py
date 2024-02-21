from django.utils import timezone

from django.db import models

from mysql_member.models import Member

# Create your models here.


class Admin_log(models.Model):
    admin_name = models.ForeignKey(Member,on_delete=models.CASCADE,verbose_name='帳號')
    admin_table = models.CharField(max_length=300,verbose_name='資料表')
    admin_operate = models.CharField(max_length=300,verbose_name='操作類')
    admin_datetime = models.DateTimeField(verbose_name='操作時間',default=timezone.now)
    admin_state = models.BooleanField(default=True,verbose_name='操作狀態')
    admin_content = models.CharField(verbose_name='詳細操作',max_length=3000,default="")
    admin_exception = models.CharField(max_length=3000,verbose_name='操作例外',null=True)
    class Meta:
        db_table = 'admin_log'
        verbose_name = "後台日誌"
        verbose_name_plural = "後台日誌"