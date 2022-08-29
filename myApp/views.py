import fractions
from itertools import count
import statistics
import sys
from threading import local
from time import time
from turtle import title
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from datetime import datetime
from django import forms
import random
import pymysql
from .models import getjob,getjob_firmware,getjob_hardware

from .forms import GETSKILL
# def sayHello4(request,username,page):
#     now = datetime.now
#     return render(request,'hello4.html',locals())#自動打包
# def sayHello(request):
#     return HttpResponse("<h3 style ='border-width:3px;border-style:dashed;border-color:#FFAC55;'>收到請求 Hellow!</h3>")
def definepage(request):
    return render(request,'heroes/index.html',locals())
def definepage_useranme(request,user_name):
    return render(request,'heroes/index.html',locals())
def search_job(request):
    return render(request,'cover/index.html',locals())
def search_job_username(request,user_name):
    return render(request,'cover/index.html',locals())
def search_job_skill(request):
    x = {}
    if request.method== 'GET':
        get_skill = request.GET['get_skill'].lower()
        type_skill = request.GET['job']
        user_name = request.GET['user_name']
        get_local =request.GET['get_local'].replace(" ","")
        try:
            page = request.GET['page'].split(" ")
        except:
            page = request.GET['select'].split(" ")
        if(page[1]=='next'):
            page = int(page[0])+1
        elif(page[1]=='last'):
            page = int(page[0])-1
        elif(page[1]=='no'):
            page = int(page[0])
        skill = get_skill.split(" ")
        fr_job=[]
        if(type_skill =='軟體工程師'):
            max = page*20
            low = max -19
            # xxxx = getjob.objects.filter(id__range=[low,max])
            if(get_local==''):
                maxpage = len(getjob.objects.all())
                jobskill= getjob.objects.all()
            else:
                maxpage = len(getjob.objects.filter(local__icontains=get_local))
                jobskill= getjob.objects.filter(local__icontains=get_local)
            if(maxpage%20==0):
                maxpage = maxpage//20
            else:
                maxpage = maxpage//20+1
        elif(type_skill == '硬體工程師'):
            max = page*20
            low = max -19
            jobskill = getjob_hardware.objects.all()
            maxpage = len(getjob_hardware.objects.all())
            if(maxpage%20==0):
                maxpage = maxpage//20
            else:
                maxpage = maxpage//20+1
        elif(type_skill =='韌體工程師'):
            max = page*20
            low = max -19
            jobskill=  getjob_firmware.objects.all()
            maxpage = len(getjob_firmware.objects.all())
            if(maxpage%20==0):
                maxpage = maxpage//20
            else:
                maxpage = maxpage//20+1
        for i in range(0,len(jobskill)):
                if(jobskill[i].website == '104'):
                    skill104 = jobskill[i].skill.lower().split("、")
                    fraction = 0
                    for z in skill104:
                        if(z.lower() in skill):
                            fraction +=1
                        elif z =='不拘':
                            fraction = -100000
                        else:
                            fraction -=20
                    x[jobskill[i]] =fraction
                else:
                    skill1111 = jobskill[i].skill.lower().split(" ")
                    fraction = 0
                    for z in skill1111:
                        if(z in skill):
                            fraction +=1
                        elif z =='無':
                            fraction = -100000
                        else:
                            fraction -=20
                    x [jobskill[i]] =fraction
        y = dict(sorted(x.items(),key=lambda y:y[1],reverse=True))
        dict_number = dict_slice(y,low,max)
        dictx={
            'get_skill':get_skill,
            'type_skill':type_skill,
            'user_name':user_name,
            'page':page,
            'skill':skill,
            'maxpage':maxpage,
            'dict_number':dict_number,
            'get_local':get_local,
        }
        return render(request,'search_job/search.html',dictx)
def dict_slice(dictzz,start,end):
    dict_keyx = list(dictzz.keys())[start:end]
    dict_page= {}
    for i in dict_keyx:
        dict_page[i] = dictzz[i]
    return dict_page


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
