from turtle import title
from django.db import models
import threading
import time
from django.db import transaction
from django.utils import timezone
# Create your models here.

class getjob(models.Model):
    date =models.DateField(default='無')
    title = models.CharField(max_length=200,null=False)
    local = models.CharField(max_length=300,null=False)
    content = models.CharField(max_length=5000,null=False)
    salary = models.CharField(max_length=150,null=False)
    company = models.CharField(max_length=600,null=False)
    href = models.CharField(max_length=100,null=False)
    experience = models.CharField(max_length=200,default=None)
    Education =  models.CharField(max_length=200,default=None)
    department = models.CharField(max_length=200,default=None)
    skill = models.CharField(max_length=600,default=None)
    language = models.CharField(max_length=600,default=None)
    Additional_conditions = models.CharField(max_length=3000,default=None)
    other = models.CharField(max_length=3000,default=None)
    website = models.CharField(max_length=45,default=None)
    class Meta:
        db_table = 'get_job'