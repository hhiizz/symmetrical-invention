from itertools import count
from time import time
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import random
# def sayHello4(request,username,page):
#     now = datetime.now
#     return render(request,'hello4.html',locals())#自動打包
# def sayHello(request):
#     return HttpResponse("<h3 style ='border-width:3px;border-style:dashed;border-color:#FFAC55;'>收到請求 Hellow!</h3>")
def definepage(request):
    return render(request,'cover/index.html',locals())
# def sayHello(request,username,page):
#     username =username
#     page = page
#     now = datetime.now
#     return render(request,'hello3.html',locals())#自動打包
# def test_dict(request):
#     dict = {'Key1':123,'Key2':456}
#     return render(request,'hello4.html',locals())
# def dice(request):
#     dice = {'no':random.randint(1,6)}
#     return render(request,'dice.html',locals())#locals --> ['dice': {'no':random.randint(1,6)}]-->{{dice.no}}key.value({'no':random.randint(1,6)}).key
# def dice2(request):
#     dice = {'no1': random.randint(1,6),
#             'no2': random.randint(1,6),
#             'no3': random.randint(1,6),}
#     return render(request,'dice2.html',locals())
# times = 0
# def dice3(request,username):
#     global times
#     times+=1
#     username = username
#     dict_no = {'no': random.randint(1,6)}
#     local_times = times
#     return render(request,'dice3.html',locals())
# emp_count = 0
# def show(request):
#     person1={"name":"Amy","phone":"049-1234567","age":20}
#     person2={"name":"Jack","phone":"02-4455666","age":25}
#     person3={"name":"Nacy","phone":"04-9876543","age":17}
#     persons=[person1,person2,person3]
#     night1 = {}
#     night2 = {}
#     night3 = {}
#     night4 = {}
#     night5 = {}
#     night6 = {}
#     night7 = {}
#     night8 = {}
#     night9 = {}
#     counts =1
#     for i in range(1,10):
#         for k in range(1,10):
#             if(i==1):
#                 night1['number'+str(k)] = str(k) +" * "+str(i)+" = "+str(i*k)
#             if(i==2):
#                 night2['number'+str(k)] = str(k) +" * "+str(i)+" = "+str(i*k)
#             if(i==3):
#                 night3['number'+str(k)] = str(k) +" * "+str(i)+" = "+str(i*k)
#             if(i==4):
#                 night4['number'+str(k)] = str(k) +" * "+str(i)+" = "+str(i*k)
#             if(i==5):
#                 night5['number'+str(k)] = str(k) +" * "+str(i)+" = "+str(i*k)
#             if(i==6):
#                 night6['number'+str(k)] = str(k) +" * "+str(i)+" = "+str(i*k)
#             if(i==7):
#                 night7['number'+str(k)] = str(k) +" * "+str(i)+" = "+str(i*k)
#             if(i==8):
#                 night8['number'+str(k)] = str(k) +" * "+str(i)+" = "+str(i*k)
#             if(i==9):
#                 night9['number'+str(k)] = str(k) +" * "+str(i)+" = "+str(i*k)
#     night = [night1,night2,night3,night4,night5,night6,night7,night8,night9]
#     return render(request,"show.html",locals())
# def filter(request):
#     return render(request,'filter.html',locals())
# Create your views here.
