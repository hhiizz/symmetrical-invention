from django.db import models
from myApp.models import getjob,getjob_firmware,getjob_hardware
from mysql_member.models import Member
# Create your models here.

# class Like(models.Model):
#     user_name = models.ForeignKey(Member,on_delete=models.CASCADE,default="")
#     job_href =  models.ForeignKey(,on_delete=models.CASCADE,default="")