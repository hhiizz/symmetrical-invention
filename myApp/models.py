from django.db import models
import threading
import time
from django.db import transaction
from django.utils import timezone
# Create your models here.
class Userinfo(models.Model):
    '''
    建立兩個欄位，最大長度為32，型別是char
    '''
    stock = models.IntegerField(default=0)
    user = models.CharField(max_length= 32,default=None)
    pwd = models.CharField(max_length= 32,default=None)
    datatime = models.DateField(default=timezone.now)