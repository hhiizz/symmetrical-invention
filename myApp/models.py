from datetime import datetime
from tabnanny import verbose
from turtle import title
from django.db import models
import threading
import time
from django.db import transaction
from django.utils import timezone
from dirtyfields import DirtyFieldsMixin
# Create your models here.
class total_type(DirtyFieldsMixin,models.Model):
    total_type_name = models.CharField(max_length=300,verbose_name='總類別表',unique=True)
    class Meta:
        db_table = 'total_type'
        verbose_name = "總類別表"
        verbose_name_plural = "總類別表"

class Job_type(DirtyFieldsMixin,models.Model):
    job_id = models.IntegerField(verbose_name='id',unique=True)
    type_name = models.CharField(max_length=300,primary_key=True,verbose_name='類名稱')
    type_url_1111 = models.CharField(max_length=2000,verbose_name='url_1111',default='null')
    type_url_104 = models.CharField(max_length=2000,verbose_name='url_104',default='null')
    total_type_name = models.ForeignKey(total_type,on_delete=models.CASCADE,null=True,verbose_name='總類名稱',db_column='total_type_name')
    class Meta:
        db_table = 'job_type'
        verbose_name = "工作類別"
        verbose_name_plural = "工作類別"
        

class getjob(DirtyFieldsMixin,models.Model):
    jobid = models.AutoField(primary_key=True)
    date =models.DateField(default='無',verbose_name='發布日期')
    get_website_id = models.CharField(max_length=300,unique=True,verbose_name='工作編號',null=False,default="")
    type = models.ForeignKey(Job_type,on_delete=models.CASCADE,null=True,verbose_name='工作類型',db_column='type')
    title = models.CharField(max_length=200,null=False,verbose_name='標題')
    local = models.CharField(max_length=300,null=False,verbose_name='工作地點')
    content = models.CharField(max_length=5000,null=False,verbose_name='工作內容')
    salary = models.CharField(max_length=150,null=False,verbose_name='薪資')
    salary_int = models.IntegerField(default=0,verbose_name="薪水值")
    company = models.CharField(max_length=600,null=False,verbose_name='公司')
    href = models.CharField(max_length=100,null=False,verbose_name='工作連結')
    experience = models.CharField(max_length=200,default=None,verbose_name='經驗要求')
    Education =  models.CharField(max_length=200,default=None,verbose_name='學歷限制')
    department = models.CharField(max_length=200,default=None,verbose_name='部門')
    skill = models.CharField(max_length=600,default=None,verbose_name='所需技能')
    language = models.CharField(max_length=600,default=None,verbose_name='語言限制')
    Additional_conditions = models.CharField(max_length=3000,default=None,verbose_name='附加條件')
    other = models.CharField(max_length=3000,default=None,verbose_name='其他')
    website = models.CharField(max_length=45,default=None,verbose_name='網站來源')
    certificate = models.CharField(max_length=700,default="不拘")
    class Meta:
        db_table = 'job_table'
        verbose_name = "職缺管理"
        verbose_name_plural = "職缺管理"

class crawler(DirtyFieldsMixin,models.Model):
    crawler_id = models.AutoField(verbose_name='id',primary_key=True)
    crawler_date =models.DateTimeField(verbose_name='時間',default=timezone.now)
    crawler_type = models.ForeignKey(Job_type,on_delete=models.CASCADE,null=True,verbose_name='爬取工作類型',db_column='crawler_type')
    crawler_website = models.CharField(max_length=200,null=False,verbose_name='爬取網站')
    crawler_count = models.CharField(max_length=300,null=False,verbose_name='數量')
    crawler_total_count  = models.IntegerField(default=0,verbose_name="爬取總數")
    crawler_state = models.BooleanField(null=False,verbose_name='狀態',default=True)
    crawler_contents = models.CharField(max_length=2300,null=True,verbose_name='詳細內容')
    class Meta:
        db_table = 'crawler_log'
        verbose_name = "爬蟲日誌"
        verbose_name_plural = "爬蟲日誌"

class Popular_searches(DirtyFieldsMixin,models.Model):
    Popular_id = models.AutoField(verbose_name='id',primary_key=True)
    Popular_skill = models.CharField(max_length = 300,verbose_name='skill')
    Popular_count = models.IntegerField(verbose_name='次數')
    Popular_type = models.ForeignKey(Job_type,on_delete=models.CASCADE,null=True,verbose_name='工作類',db_column='popular_type')
    class Meta:
        db_table = 'Popular_searches'
        constraints = [
            models.UniqueConstraint(fields=['Popular_skill', 'Popular_type'], name='Popular_skill_type_unique')
        ]
class trend(DirtyFieldsMixin,models.Model):
    trend_id = models.AutoField(verbose_name='id',primary_key=True)
    trend_skill =  models.CharField(max_length = 230,verbose_name='趨勢技能')
    trend_count = models.IntegerField(null=False,verbose_name='次數')
    trend_date = models.DateField(verbose_name='時間',default=timezone.now)
    trend_type =  models.ForeignKey(Job_type,on_delete=models.CASCADE,null=True,verbose_name='技能工作類型',db_column='trend_type')
    class Meta:
        db_table = 'trend'
        verbose_name = "趨勢分析"
        verbose_name_plural = "趨勢分析"
