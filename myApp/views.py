from importlib.metadata import requires
from lib2to3.pytree import type_repr
import re
import statistics
import calendar
import sys
from threading import local
from time import strftime, time
from turtle import title
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import datetime
from django import forms
import json
import random
import pymysql
from mysql_member.models import Member, Popular_job
import user
from user.models import Like, Notice, Recommend
from .models import Job_type, getjob,Popular_searches, total_type, trend,crawler
from django.utils import timezone
import pytz
from django.db.models import Sum,Count
from .forms import GETSKILL
from django.db.models import Q

def first_ok(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        user_name = request.session['username']
        power =  request.session['power']
        count_notice =request.session['notice']
        first = '0'
        tit = get_suggest()
        return render(request,'heroes/index.html',locals())
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def definepage(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        user_name = request.session['username']
        power =  request.session['power']
        count_notice =request.session['notice']
        tit = get_suggest()
        return render(request,'heroes/index.html',locals())
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})




def definepage_session(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        user_name = request.session['username']
        power =  request.session['power']
        count_notice =request.session['notice']
        zz = Like.objects.filter(like_type='Like').values('like_jobid').annotate(count=Count('like_jobid')).order_by('-count')[:10]
        tit = get_suggest()
        return render(request,'heroes/index.html',locals())
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})



def search_job(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        user_name = request.session['username']
        power =  request.session['power']
        count_notice =request.session['notice']
    job_type = dict(Job_type.objects.values_list("type_name","job_id"))
    popular = {}
    for i in job_type.keys():
        popular[job_type[i]] = Popular_searches.objects.filter(Popular_type_id = i).annotate(Sum('Popular_count')).values('Popular_skill','Popular_count__sum').order_by('-Popular_count__sum')[0:15]
    dict_jobname = {}
    type = total_type.objects.filter()
    for i in type:
        dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
    local =  get_local_fun()
    return render(request,'cover/index.html',locals())


def search_job_skill(request):
    x = {}
    dict_register = {}
    dict_skill = {}
    user_name = request.session.get('username',None)
    if user_name != None and not  Member.objects.filter(username=request.session['username']).exists() :
        user_name = None
    get_skill = request.GET['get_skill'].lower().replace(',',"、").split("、")
    type_skill = request.GET['job']
    extends_local = request.GET.get("extends_local","")
    extends_type = request.GET.get("extends_type","")
    get_local = request.GET.get('get_local','')
    skill_hot = request.GET.get('skill_hot',"")
    get_sorted = request.GET.get('sorted',"")
    certificate_user = request.GET.get('certificate_user','')
    search_keyword = request.GET.get('search_keyword',"").replace(',',"、").split('、')
    salary_select = request.GET.get('salary',"")
    certificate_select = request.GET.get('certificate_select','')
    if(salary_select == 'change_salary' and "Customize_salary" in request.GET):
        if("Customize_salary" in request.GET):
            salary_select = request.GET['Customize_salary']
    else:
        salary_select = ''
    if(len(get_skill)>100):
        message = '輸入異常!'
        return render(request,'cover/index.html',locals())
    try:
        page = request.GET['page'].split(" ")
    except:
        page = request.GET['select'].split(" ")
    select_date = request.GET.get('date',"")
    select_Education = request.GET.get('Education','')
    select_experience = request.GET.get('experience','')
    if(select_experience == 'Customize'):
        Customize = request.GET.get('Customize',"")
        if(Customize == ""):
            select_experience = ""
    else:
        Customize = ""
    # if(select_date!=''):
    #     today = datetime.datetime.now()-datetime.timedelta(days=int(select_date))
    #     today = today.strftime('%Y-%m-%d')
    if(page[1]=='next'):
        page = int(page[0])+1
    elif(page[1]=='last'):
        page = int(page[0])-1
    elif(page[1]=='no'):
        page = int(page[0])
    skill = get_skill
    max = page*20
    low = max -20
    job_certificate = set()
    if(skill_hot != ""):
        q_objects =(Q(type=type_skill)) & (Q(skill__icontains= "、"+skill_hot + "、") | Q(skill__icontains=skill_hot+"、") |Q(skill = skill_hot))
        jobskill = getjob.objects.filter(q_objects)
        dict_register ['skill_hot'] = skill_hot
    else:
        jobskill= getjob.objects.filter(type=type_skill)
    if(get_local != ""):
        get_local = json.loads(get_local)
        q_objects = Q()
        for k,v in get_local.items():
            for i in v:
                if(k == i):
                    q_objects |= Q(local__icontains=i)
                else:
                    q_objects |= Q(local__icontains=k+i) # 使用 |= 來建立多個OR條件
        jobskill = jobskill.filter(q_objects) # 將Q物件應用於查詢
        get_local=json.dumps(get_local, ensure_ascii=False)
    else:
        extends_local = ""
        extends_type  = ""
    if(search_keyword!=""):
        for i in search_keyword:
            q_objects = Q()
            q_objects =Q(title__icontains =i) | Q(content__icontains =i) | Q(Additional_conditions__icontains =i) |Q(skill__icontains =i)
        jobskill = jobskill.filter(q_objects)
        
    if(select_date!=""):
        today = datetime.datetime.now()-datetime.timedelta(days=int(select_date))
        today = today.strftime('%Y-%m-%d')
        jobskill= jobskill.filter(date__gte=today)
        dict_register['select_date'] =select_date
    if(select_experience=='Customize'):
        range_exper = [ str(i)+'年以上工作經驗' for i in range(1,int(Customize)+1)]
        range_exper2= [ str(i)+'年以上' for i in range(1,int(Customize)+1)]
        range_exper.append('半年以上的工作經歷')
        jobskill= jobskill.filter(experience__in=range_exper) | jobskill.filter(experience__in=range_exper2) | jobskill.filter(experience='不拘') | jobskill.filter(experience='經歷不拘')
    elif(select_experience =="noexper"):
        jobskill= jobskill.filter(experience='不拘') | jobskill.filter(experience='經歷不拘') | jobskill.filter(experience='無工作經驗可')
    if(select_Education=='secondary'):
        jobskill= jobskill.filter(Education__icontains ='國中') | jobskill.filter(Education__icontains ='學歷不拘') | jobskill.filter(Education__icontains ='不拘')
    elif(select_Education=='highschool'):
        jobskill= jobskill.filter(Education__icontains ='國中') | jobskill.filter(Education__icontains ='高中') | jobskill.filter(Education__icontains ='學歷不拘') | jobskill.filter(Education__icontains ='不拘')
    elif(select_Education=='Specialist'or select_Education=='University'):
        jobskill= jobskill.filter(Education__icontains ='國中') | jobskill.filter(Education__icontains ='高中') | jobskill.filter(Education__icontains ='大學') | jobskill.filter(Education__icontains ='專科') |jobskill.filter(Education__icontains ='學歷不拘') | jobskill.filter(Education__icontains ='不拘')
    elif(select_Education=='master'):
        jobskill= jobskill.filter(Education__icontains ='國中') | jobskill.filter(Education__icontains ='高中') | jobskill.filter(Education__icontains ='大學') | jobskill.filter(Education__icontains ='專科') | jobskill.filter(Education__icontains ='碩士') | jobskill.filter(Education__icontains ='學歷不拘') | jobskill.filter(Education__icontains ='不拘')
    if(certificate_user != ''):
        q_objects = Q()
        certificate_user = certificate_user.split('、')
    if(salary_select != ''):
        jobskill = jobskill.filter(salary_int__gte = int(salary_select))
        dict_register['salary_select'] =salary_select
    if(certificate_select != ''):
        jobskill = jobskill.filter(certificate = '不拘')
        dict_register['certificate_select'] = certificate_select
    if(get_skill != [""]):
        for i in range(0,len(jobskill)):
            skilltoto = jobskill[i].skill.lower().split("、")
            fraction = 0
            certificate_fraction = 0
            for z in skilltoto:
                if(z.lower() in skill):
                    fraction +=2
                    dict_skill[z.title()] = 'yes'
                elif z =='不拘' or  z =='無':
                    fraction = -float('Inf')
                else:
                    fraction -=10
                    dict_skill[z.title()]  = 'no'
                    jobskill[i].experience
            if(fraction == len(skilltoto)*-10):
                fraction = -10000*len(skilltoto)
            certificate =jobskill[i].certificate.upper().split('、')
            if(jobskill[i].certificate != '不拘'):
                for certif in certificate:
                    if(not certif.upper() in certificate_user):
                        certificate_fraction-=10
                        job_certificate.add(certif)
                    else:
                        certificate_fraction+=2
                if(certificate_fraction == len(certificate)*-10):
                    certificate_fraction = -100000+len(certificate)*-10
            else:
                certificate_fraction = -100000
            if get_sorted != ""  and len(skilltoto)*2 == fraction:
                fraction = float('Inf')                                 # 排序
            if get_sorted != ""  and len(certificate)*2 == certificate_fraction:
                certificate_fraction = float('Inf')
                
            if(fraction != -float('Inf') and fraction != -10000*len(skilltoto) or certificate_fraction > -100000 ):
                if(get_sorted == 'experience_max'):
                    match = re.search(r'\d+',jobskill[i].experience)
                    if match:
                        x[jobskill[i]] =[fraction,int(match.group())]
                    else:
                        x[jobskill[i]] =[fraction,0]
                elif(get_sorted == 'experience_low'):
                    match = re.search(r'\d+',jobskill[i].experience)
                    if match:
                        x[jobskill[i]] =[fraction,-int(match.group())]
                    else:
                        x[jobskill[i]] =[fraction,0]
                elif(get_sorted == 'date_max'):
                    x[jobskill[i]] =[fraction,jobskill[i].date]
                elif(get_sorted == 'certificate_suitable'):
                    x[jobskill[i]] =[fraction,certificate_fraction]
                elif(get_sorted == 'salary_suitable'):
                    x[jobskill[i]] = [fraction,jobskill[i].salary_int]
                else:
                    x[jobskill[i]] =[fraction]
                if(certificate_user != ''):
                    x[jobskill[i]].append(certificate_fraction)
                x[jobskill[i]].append(len(skilltoto))
    else:
        for i in range(0,len(jobskill)):
            cer_count =0
            skilltoto = jobskill[i].skill.lower().split("、")
            fraction = 0
            certificate_fraction = 0
            certificate =jobskill[i].certificate.upper().split('、')
            if(jobskill[i].certificate != '不拘'):
                for certif in certificate:
                    if(not certif.upper() in certificate_user):
                        certificate_fraction-=10
                        job_certificate.add(certif)
                    else:
                        certificate_fraction+=2
                        cer_count+=1
                if(certificate_fraction == len(certificate)*-10):
                    certificate_fraction = -100000+len(certificate)*-10
            else:
                certificate_fraction = -100000
            if get_sorted != ""  and len(certificate)*2 == certificate_fraction:
                certificate_fraction = float('Inf')
            for z in skilltoto:
                if z =='不拘' or  z =='無':
                    fraction = -float('Inf')
                else:
                    dict_skill[z.title()]  = 'no'
            if(get_sorted == 'experience_max'):
                match = re.search(r'\d+',jobskill[i].experience)
                if match:
                    x[jobskill[i]] =[fraction,int(match.group())]
                else:
                    x[jobskill[i]] =[fraction,0]
            elif(get_sorted == 'experience_low'):
                match = re.search(r'\d+',jobskill[i].experience)
                if match:
                    x[jobskill[i]] =[fraction,-int(match.group())]
                else:
                    x[jobskill[i]] =[fraction,0]
            elif(get_sorted == 'date_max'):
                x[jobskill[i]] =[fraction,jobskill[i].date]
            elif(get_sorted == 'certificate_suitable'):
                x[jobskill[i]] =[fraction,certificate_fraction]
            elif(get_sorted == 'salary_suitable'):
                x[jobskill[i]] = [fraction,jobskill[i].salary_int]
            else:
                x[jobskill[i]] =[fraction]
            if(certificate_user != ''):
                x[jobskill[i]].append(certificate_fraction)
            x[jobskill[i]].append(len(skilltoto))
    maxpage = len(x)
    if(maxpage%20==0):
        maxpage = maxpage//20
    else:
        maxpage = maxpage//20+1
    dict_skill = dict(sorted(dict_skill.items(),key=lambda x:(x[1],x[0]),reverse=True))
    select_key_name = list(dict_skill.keys())
    if(get_skill !=""):
        for i in get_skill:
            if(i.title() in select_key_name):
                xx = Popular_searches.objects.filter(Popular_skill__icontains=i.title(),Popular_type_id=type_skill)
                if(len(xx)!=0):
                    xx.update(Popular_count=xx[0].Popular_count+1)
                else:
                    xx = Popular_searches(Popular_skill=i,Popular_count=1,Popular_type_id=type_skill)
                    xx.save()
    dict_jobname = {}
    for i in total_type.objects.filter():
        dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
    if(certificate_user != '' and get_sorted != ''):
        y = dict(sorted(x.items(),key=lambda y:(y[1][2],y[1][0],y[1][1],y[1][3]),reverse=True))
    elif(get_sorted != ""):
        y = dict(sorted(x.items(),key=lambda y:(y[1][0],y[1][1],y[1][2]),reverse=True))
    elif(certificate_user != ''):
        y = dict(sorted(x.items(),key=lambda y:(y[1][1],y[1][0],y[1][2]),reverse=True))
    else:   
        y = dict(sorted(x.items(),key=lambda y:y[1][0],reverse=True))
    dict_number = dict_slice(y,low,max,user_name) 
    job_certificate = list(job_certificate)
    job_certificate.sort()
    dictx={
        'get_skill':"、".join(get_skill),
        'type_skill':type_skill,
        'page':page,
        'maxpage':maxpage,
        'dict_number':dict_number,
        'get_local':get_local,
        'dict_skill':dict_skill,
        'select_Education':select_Education,
        'select_experience':select_experience,
        'search_keyword':request.GET.get('search_keyword',""),
        'Customize':Customize,
        'dict_jobname':dict_jobname,
        "local": get_local_fun(),
        "extends_local":extends_local,
        "extends_type":extends_type,
        "get_sorted":get_sorted,
        'job_certificate':job_certificate,
        'certificate_user':certificate_user,
    }
    if(user_name != None):
        dictx['user_name'] = user_name
        dictx['power'] = request.session['power']
    dictx.update(dict_register)
    return render(request,'search_job/search.html',dictx)


























def dict_slice(dictzz,start,end,user_name):
    dict_keyx = list(dictzz.keys())[start:end]
    dict_page= {}
    popular_job_list =  list(Popular_job.objects.filter(popular_job_user_id = user_name).values_list('popular_jobid',flat=True))
    for i in dict_keyx:
        count = Popular_job.objects.filter(popular_jobid_id=i.jobid).count()
        x= Like.objects.filter(like_user_name_id = user_name,like_jobid_id = i.jobid, like_type='like').exists()
        if( not x):
            if i.jobid in popular_job_list:
                dict_page[i] = {"1":{"love":'no','recommend':'yes',"count":count}}
            else:
                dict_page[i] = {"1":{"love":'no','recommend':'no',"count":count}}
        else:
            if i.jobid in popular_job_list:
                dict_page[i] = {"1":{"love":'yes','recommend':'yes',"count":count}}
            else:
               dict_page[i] = {"1":{"love":'yes','recommend':'no',"count":count}}
    return dict_page
# def dict_slice_two(dictzz,start,end,user_name):
#     dict_keyx = list(dictzz.keys())[start:end]
#     dict_page= {}
#     popular_job_list =  list(Popular_job.objects.filter(popular_job_user_id = user_name).values_list('popular_jobid',flat=True))
#     for i in dict_keyx:
#         count = Popular_job.objects.filter(popular_jobid_id=i.jobid).count()
#         x= Like.objects.filter(like_user_name_id = user_name,like_jobid_id = i.jobid, like_type='like').exists()
#         if(x):
#             if i.jobid in popular_job_list:
#                 dict_page[i] = {"1":{"love":'no','recommend':'yes',"count":count}}
#             else:
#                 dict_page[i] = {"1":{"love":'no','recommend':'no',"count":count}}
#         else:
#             if i.jobid in popular_job_list:
#                 dict_page[i] = {"1":{"love":'yes','recommend':'yes',"count":count}}
#             else:
#                dict_page[i] = {"1":{"love":'yes','recommend':'no',"count":count}}
#     return dict_page
# def dict_slice_three(dictzz,start,end,user_name):
#     dict_keyx = list(dictzz.keys())[start:end]
#     dict_page= {}
#     popular_job_list =  list(Popular_job.objects.filter(popular_job_user_id = user_name).values_list('popular_jobid',flat=True))
#     for i in dict_keyx:
#         dict_job_love = {}
#         count = Popular_job.objects.filter(popular_jobid_id=i.jobid).count()
#         x= Like.objects.filter(like_user_name_id = user_name,like_jobid_id = i.jobid, like_type='like').exists()
#         if(x):
#             if i.jobid in popular_job_list:
#                 dict_page[i] = {"1":{"love":'no','recommend':'yes',"count":count}}
#             else:
#                 dict_page[i] = {"1":{"love":'no','recommend':'no',"count":count}}
#         else:
#             if i.jobid in popular_job_list:
#                 dict_page[i] = {"1":{"love":'yes','recommend':'yes',"count":count}}
#             else:
#                dict_page[i] = {"1":{"love":'yes','recommend':'no',"count":count}}
#         return dict_page


def company(request):
    dict_register = {}
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        count_notice =request.session['notice']
        power =  request.session['power']
        user_name = request.session['username']
        dict_register['count_notice'] = count_notice
        dict_register['power'] = power
        dict_register['user_name'] = user_name
    dict_skill ={}
    company_name = request.GET.get('company_name','')
    get_skill = request.GET['get_skill'].lower().replace(',',"、").split("、")
    type_skill = request.GET['job']
    get_local =request.GET.get('get_local',"")
    extends_local = request.GET.get("extends_local","")
    extends_type = request.GET.get("extends_type","")
    select_date = request.GET.get('date',"")
    select_Education = request.GET.get('Education','')
    select_experience = request.GET.get('experience','')
    get_sorted = request.GET.get('sorted',"")
    certificate_user = request.GET.get('certificate_user','')
    job_certificate = set()
    if(select_experience == 'Customize'):
        Customize = request.GET.get('Customize',"")
        if(Customize == ""):
            select_experience = ""
    else:
        Customize = ""
    salary_select = request.GET.get('salary',"")
    certificate_select = request.GET.get('certificate_select','')
    if(salary_select == 'change_salary' and "Customize_salary" in request.GET):
        if("Customize_salary" in request.GET):
            salary_select = request.GET['Customize_salary']
    else:
        salary_select = ''
    
    if(get_local != ""):
        get_local = json.loads(get_local)
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
    skill = get_skill
    jobskill= getjob.objects.filter(type=type_skill)
    if(company_name !=''):
        jobskill= jobskill.filter(company=company_name)
        extends_local = ""
        extends_type  = ""
    if(get_local != ''):
        q_objects = Q()
        for k,v in get_local.items():
            for i in v:
                if( i== k):
                    q_objects |= Q(local__icontains=k)
                else:
                    q_objects |= Q(local__icontains=k+i) # 使用 |= 來建立多個OR條件
        jobskill= jobskill.filter(q_objects)
    if(select_date!=""):
        today = datetime.datetime.now()-datetime.timedelta(days=int(select_date))
        today = today.strftime('%Y-%m-%d')
        jobskill= jobskill.filter(date__gte=today)
        dict_register['select_date'] =select_date
    if(select_experience=='Customize'):
        range_exper = [ str(i)+'年以上工作經驗' for i in range(1,int(Customize)+1)]
        range_exper2= [ str(i)+'年以上' for i in range(1,int(Customize)+1)]
        range_exper.append('半年以上的工作經歷')
        dict_register['Customize'] = Customize
        jobskill= jobskill.filter(experience__in=range_exper) | jobskill.filter(experience__in=range_exper2) | jobskill.filter(experience='不拘') | jobskill.filter(experience='經歷不拘')
    elif(select_experience =="noexper"):
        jobskill= jobskill.filter(experience='不拘') | jobskill.filter(experience='經歷不拘') | jobskill.filter(experience='無工作經驗可')
    if(select_Education=='secondary'):
        jobskill= jobskill.filter(Education__icontains ='國中') | jobskill.filter(Education__icontains ='學歷不拘') | jobskill.filter(Education__icontains ='不拘')
    elif(select_Education=='highschool'):
        jobskill= jobskill.filter(Education__icontains ='國中') | jobskill.filter(Education__icontains ='高中') | jobskill.filter(Education__icontains ='學歷不拘') | jobskill.filter(Education__icontains ='不拘')
    elif(select_Education=='Specialist'or select_Education=='University'):
        jobskill= jobskill.filter(Education__icontains ='國中') | jobskill.filter(Education__icontains ='高中') | jobskill.filter(Education__icontains ='大學') | jobskill.filter(Education__icontains ='專科') |jobskill.filter(Education__icontains ='學歷不拘') | jobskill.filter(Education__icontains ='不拘')
    elif(select_Education=='master'):
        jobskill= jobskill.filter(Education__icontains ='國中') | jobskill.filter(Education__icontains ='高中') | jobskill.filter(Education__icontains ='大學') | jobskill.filter(Education__icontains ='專科') | jobskill.filter(Education__icontains ='碩士') | jobskill.filter(Education__icontains ='學歷不拘') | jobskill.filter(Education__icontains ='不拘')
    if(select_experience != ''):
        dict_register['select_experience'] = select_experience
    if(select_Education != ''):
        dict_register['select_Education'] = select_Education
    if(certificate_user != ''):
        q_objects = Q()
        certificate_user = certificate_user.split('、')
        dict_register['certificate_user'] = certificate_user
    if(salary_select != ''):
        jobskill = jobskill.filter(salary_int__gte = int(salary_select))
        dict_register['salary_select'] =salary_select
    if(certificate_select != ''):
        jobskill = jobskill.filter(certificate = '不拘')
        dict_register['certificate_select'] = certificate_select
    maxpage = len(jobskill)
    dict_jobname = {}
    for i in total_type.objects.filter():
        dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
    dict_company = {}
    max = page*10
    low = max -10
    for i in range(0,len(jobskill)):
        dict_fractioin = {}
        skilltoto = jobskill[i].skill.lower().split("、")
        fraction = 0
        cer_count =0
        certificate_fraction =0
        fraction_skill =0
        certificate =jobskill[i].certificate.upper().split('、')
        if(jobskill[i].certificate != '不拘'):
            for certif in certificate:
                if(not certif.upper() in certificate_user):
                    certificate_fraction-=10
                    job_certificate.add(certif)
                else:
                    certificate_fraction+=2
                    cer_count+=1
            if(certificate_fraction == len(certificate)*-10):
                certificate_fraction = -float('Inf')
        else:
            certificate_fraction = -float('Inf')
        for z in skilltoto:
            if z =='不拘' or  z =='無':
                fraction = float('Inf')
                break
            elif(not z.lower() in skill):
                fraction +=1
                fraction_skill-=10
                dict_skill[z.title()] = 'no'
            else:
                fraction_skill+=2
                dict_skill[z.title()] = 'yes'
        if get_sorted != ""  and len(skilltoto)*2 == fraction_skill:
            fraction_skill = float('Inf')                                 # 排序
        if get_sorted != ""  and len(certificate)*2 == certificate_fraction:
            certificate_fraction = float('Inf')
        if(fraction ==0):
            statue = 0
        elif(fraction <= len(skilltoto)/3):
            statue = -30
        elif(fraction <= len(skilltoto)/2):
            statue = -70
        elif fraction == float('Inf'):
            statue = -101
        else:
            statue = -100
        if(get_skill != ['']):
            if(certificate_fraction == -float('Inf') and (fraction == float('Inf') or fraction == len(skilltoto) ) ):
                continue
        if(get_sorted == 'experience_max'):
            match = re.search(r'\d+',jobskill[i].experience)
            if match:
                dict_fractioin['experience'] =int(match.group())
            else:
                dict_fractioin['experience'] =0
            dict_register['get_sorted'] =get_sorted 
        elif(get_sorted == 'experience_low'):
            match = re.search(r'\d+',jobskill[i].experience)
            if match:
                dict_fractioin['experience'] =-int(match.group())
            else:
                dict_fractioin['experience'] =0
            dict_register['get_sorted'] =get_sorted
        elif(get_sorted == 'date_max'):
            dict_fractioin['date'] =jobskill[i].date
            dict_register['get_sorted'] =get_sorted
        elif(get_sorted == 'certificate_suitable'):
            dict_fractioin['certificate_fraction'] =certificate_fraction
            dict_register['get_sorted'] =get_sorted
        elif(get_sorted == 'salary_suitable'):
            dict_fractioin['salary_int'] =jobskill[i].salary_int
            dict_register['get_sorted'] =get_sorted 
        dict_fractioin['job'] = jobskill[i].title
        dict_fractioin['state'] = statue
        dict_fractioin['salary'] =jobskill[i].salary
        dict_fractioin['href'] = jobskill[i].href
        dict_fractioin['website'] = jobskill[i].website
        dict_fractioin['skill'] = jobskill[i].skill
        dict_fractioin['fraction_skill'] = fraction_skill
        dict_fractioin['skill_count'] = len(skilltoto)
        if(jobskill[i].certificate != '不拘'):
            dict_fractioin['certificate'] = jobskill[i].certificate
        if(certificate_user != ''):
            dict_fractioin['certificate_fraction'] =certificate_fraction
        try:
            dict_company[jobskill[i].company]['dict_fractioin'].append(dict_fractioin)
        except Exception:
            dict_company[jobskill[i].company] = {'dict_fractioin':[dict_fractioin],
                                                    "certitficate_count":0,
                                                    'good_state':0,
                                                    'soso_state':0,
                                                    'bad_state':0,
                                                    'low_state':0,
                                                    'none_state':0}
        if(statue == 0):
            dict_company[jobskill[i].company]['good_state']+=1
        elif(statue == -30):
            dict_company[jobskill[i].company]['soso_state']+=1
        elif(statue == -70):
            dict_company[jobskill[i].company]['bad_state']+=1
        elif(statue == -100):
            dict_company[jobskill[i].company]['low_state']+=1
        else:
            dict_company[jobskill[i].company]['none_state']+=1
        if(certificate_fraction != -float('Inf')):
            dict_company[jobskill[i].company]['certitficate_count']+=1
    maxpage = len(dict_company)
    if(maxpage%10==0):
        maxpage = maxpage//10
    else:
        maxpage = maxpage//10+1
    dict_company = dict(sorted(dict_company.items(), key=lambda i:(i[1]['certitficate_count'],i[1]['good_state'],i[1]['soso_state'],i[1]['bad_state'],i[1]['low_state'],i[1]['none_state'],len(i[1]['dict_fractioin'])),reverse=True))#對dict排序一整體評分,數量
    company_name = set(getjob.objects.filter(type = type_skill).values_list('company',flat=True))
    dict_company =dict(list(dict_company.items())[low:max])
    if(len(certificate_user) != 0 ):
        if(get_sorted == 'experience_max' or get_sorted == 'experience_low'):
            for i,v in dict_company.items():
                dict_company[i] = sorted(v['dict_fractioin'],key = lambda e:(e.__getitem__('certificate_fraction'),e.__getitem__('state'),e.__getitem__('fraction_skill'),e.__getitem__('experience'),e.__getitem__('skill_count')),reverse=True)#dict 內部排序
        elif(get_sorted == 'date_max'):
            for i,v in dict_company.items():
                dict_company[i] = sorted(v['dict_fractioin'],key = lambda e:(e.__getitem__('certificate_fraction'),e.__getitem__('state'),e.__getitem__('fraction_skill'),e.__getitem__('date'),e.__getitem__('skill_count')),reverse=True)#dict 內部排序
        elif(get_sorted == 'salary_suitable'):
            for i,v in dict_company.items():
                dict_company[i] = sorted(v['dict_fractioin'],key = lambda e:(e.__getitem__('certificate_fraction'),e.__getitem__('state'),e.__getitem__('fraction_skill'),e.__getitem__('salary_int'),e.__getitem__('skill_count')),reverse=True)#dict 內部排序
        elif(get_sorted == 'certificate_suitable'):
            for i,v in dict_company.items():
                dict_company[i] = sorted(v['dict_fractioin'],key = lambda e:(e.__getitem__('certificate_fraction'),e.__getitem__('state'),e.__getitem__('fraction_skill'),e.__getitem__('certificate_fraction'),e.__getitem__('skill_count')),reverse=True)#dict 內部排序
        else:
            for i,v in dict_company.items():
                dict_company[i] = sorted(v['dict_fractioin'],key = lambda e:(e.__getitem__('certificate_fraction'),e.__getitem__('state'),e.__getitem__('fraction_skill'),e.__getitem__('skill_count')),reverse=True)#dict 內部排序
    else:
        if(get_sorted == 'experience_max' or get_sorted == 'experience_low'):
            for i,v in dict_company.items():
                dict_company[i] = sorted(v['dict_fractioin'],key = lambda e:(e.__getitem__('state'),e.__getitem__('fraction_skill'),e.__getitem__('experience'),e.__getitem__('skill_count')),reverse=True)#dict 內部排序
        elif(get_sorted == 'date_max'):
            for i,v in dict_company.items():
                dict_company[i] = sorted(v['dict_fractioin'],key = lambda e:(e.__getitem__('state'),e.__getitem__('fraction_skill'),e.__getitem__('date'),e.__getitem__('skill_count')),reverse=True)#dict 內部排序
        elif(get_sorted == 'salary_suitable'):
            for i,v in dict_company.items():
                dict_company[i] = sorted(v['dict_fractioin'],key = lambda e:(e.__getitem__('state'),e.__getitem__('fraction_skill'),e.__getitem__('salary_int'),e.__getitem__('skill_count')),reverse=True)#dict 內部排序
        elif(get_sorted == 'certificate_suitable'):
            for i,v in dict_company.items():
                dict_company[i] = sorted(v['dict_fractioin'],key = lambda e:(e.__getitem__('state'),e.__getitem__('fraction_skill'),e.__getitem__('certificate_fraction'),e.__getitem__('skill_count')),reverse=True)#dict 內部排序
        else:
            for i,v in dict_company.items():
                dict_company[i] = sorted(v['dict_fractioin'],key = lambda e:(e.__getitem__('state'),e.__getitem__('fraction_skill'),e.__getitem__('skill_count')),reverse=True)#dict 內部排序
    if(get_local != ''):
        get_local = json.dumps(get_local, ensure_ascii=False)
    dict_skill = dict(sorted(dict_skill.items(),key=lambda x:(x[1],x[0]),reverse=True))
    select_key_name = list(dict_skill.keys())
    job_certificate = list(job_certificate)
    job_certificate.sort()
    total_dict = {
        'dict_company':dict_company,
        'get_skill':"、".join(get_skill),
        'get_local':get_local,
        'type_skill':type_skill,
        'maxpage':maxpage,
        'page':page,
        'company_name':company_name,
        'dict_jobname':dict_jobname,
        "local": get_local_fun(),
        "extends_local":extends_local,
        "extends_type":extends_type,
        'dict_skill':dict_skill,
        'job_certificate':job_certificate,
        'certificate_user':certificate_user
    }
    total_dict.update(dict_register)
    return render(request,'search_job/search_company.html',total_dict)


def trend_fun(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        count_notice =request.session['notice']
        power =  request.session['power']
        user_name = request.session['username']
    month_count = {}
    month_count_last = {}
    date_start = request.GET.get('date_start',str(datetime.date.today().year)+'-'+'01')
    date_end = request.GET.get('date_end',datetime.datetime.now().strftime('%Y-%m'))
    fun = request.GET['trend_function']
    get_skill = request.GET['get_skill'].lower().replace(',',"、").split("、")
    type_skill = request.GET['job']
    get_local =request.GET.get('get_local',"")
    extends_local = request.GET.get("extends_local","")
    extends_type = request.GET.get("extends_type","")
    if(fun == 'job_count_trend'):
        count_job = {}
        growin_up = []
        year_start = int(datetime.datetime.strptime(date_start,'%Y-%m').year)
        month_start = int(datetime.datetime.strptime(date_start,'%Y-%m').month)                                                                                                 #因會少一個月所以加一來確保
        count = (int(datetime.datetime.strptime(date_end,'%Y-%m').year)-int(datetime.datetime.strptime(date_start,'%Y-%m').year))*12 + (int(datetime.datetime.strptime(date_end,'%Y-%m').month+1)-int(datetime.datetime.strptime(date_start,'%Y-%m').month))
        for i in range(count):
            if(month_start>12):
                month_start=1
                year_start+=1
            count = (crawler.objects.filter(crawler_type = type_skill,crawler_date__range = [datetime.datetime(year_start, month_start, 1, 0, 0, 0, tzinfo=pytz.timezone('Asia/Taipei')),datetime.datetime(year_start,month_start,calendar.monthrange(year_start,month_start)[1], 23, 59,59, tzinfo=pytz.timezone('Asia/Taipei'))]).aggregate(Sum('crawler_count')))['crawler_count__sum']
            last_count = (crawler.objects.filter(crawler_type = type_skill,crawler_date__range = [datetime.datetime(year_start-1, month_start, 1, 0, 0, 0,tzinfo=pytz.timezone('Asia/Taipei')),datetime.datetime(year_start-1,month_start,calendar.monthrange(year_start-1,month_start)[1], 23, 59,59, tzinfo=pytz.timezone('Asia/Taipei'))]).aggregate(Sum('crawler_count')))['crawler_count__sum']
            if(count==None):
                count=0
            if(last_count==None):
                last_count = 0
            month_count[str(year_start)+'-'+str(month_start)]= str(count)
            month_count_last[str(year_start-1)+'-'+str(month_start)]=str(last_count)
            if(count==0 and last_count==0):
                growin_up.append('0')
            elif(last_count==0):
                growin_up.append('100')
            else:
                growin_up.append('{:.0f}'.format((count-last_count)/last_count*100))
            month_start +=1
        month_key = '、'.join(list(month_count.keys()))
        month_value = '、'.join(list(month_count.values()))
        month_last_value = '、'.join(list(month_count_last.values()))
        growin_up = '、'.join(growin_up)
        dict_jobname = {}
        for i in total_type.objects.filter():
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
        if 'username' in request.session:
            total_dict = {
                'date_start':date_start,
                'date_end':date_end,
                'month_key':month_key,
                'get_skill':"、".join(get_skill),
                'user_name':user_name,
                'get_local':get_local,
                'type_skill':type_skill,
                'month_value':month_value,
                'month_last_value':month_last_value,
                'growin_up':growin_up,
                'power':power,
                'count_notice':count_notice,
                'dict_jobname':dict_jobname,
                "extends_local":extends_local,
                "extends_type":extends_type,
            }
        else:
            total_dict = {
                'date_start':date_start,
                'date_end':date_end,
                'month_key':month_key,
                'get_skill':"、".join(get_skill),
                'get_local':get_local,
                'type_skill':type_skill,
                'month_value':month_value,
                'month_last_value':month_last_value,
                'growin_up':growin_up,
                'dict_jobname':dict_jobname,
                "extends_local":extends_local,
                "extends_type":extends_type,
            }
        return render(request,'search_job/trend.html',total_dict)
    elif(fun =='skill_picture'):
        count_skill = int(request.GET.get('count_skill',10))
        skill_count = {}
        extends_local = request.GET.get("extends_local","")
        extends_type = request.GET.get("extends_type","")
        year_start = int(datetime.datetime.strptime(date_start,'%Y-%m').year)
        month_start = int(datetime.datetime.strptime(date_start,'%Y-%m').month)
        date_start_day = date_start+'-01'
        last_date_start = str(year_start-1)+'-'+str(month_start)+'-01'
        zz = date_end.split('-')
        date_end = zz[0]+'-'+zz[1]+'-'+str(calendar.monthrange(int(zz[0]),int(zz[1]))[1])
        last_date_end = str(int(zz[0])-1)+'-'+zz[1]+'-'+str(calendar.monthrange(int(zz[0]),int(zz[1]))[1])
        skill_count_zz = trend.objects.filter(trend_type = type_skill,trend_date__range=[date_start_day,date_end]).values('trend_skill').annotate(Sum('trend_count')).order_by('-trend_count__sum')[:count_skill]
        for i in skill_count_zz:
            skill_count[i['trend_skill']] = [str(i['trend_count__sum'])]
        last_skill_dict = trend.objects.filter(trend_type = type_skill,trend_date__range=[last_date_start,last_date_end],trend_skill__in=list(skill_count.keys())).values('trend_skill').annotate(Sum('trend_count'))
        for i in last_skill_dict:
            if i['trend_skill'] in skill_count :                                                         #dict_篩選因成長路基數為0需記錄判斷陣列長度即可
                skill_count[i['trend_skill']].append(i['trend_count__sum'])
                skill_count[i['trend_skill']].append((int(skill_count[i['trend_skill']][0])-i['trend_count__sum'])/i['trend_count__sum']*100)
        last_skill_count = list(skill_count.values())
        val_now = []
        val_last = []
        growin_up = []
        color = {}
        skill_key = list(skill_count.keys())
        list_skill = get_skill
        for i in skill_key:
            if(i.lower() in list_skill):
                color[i] = 'green'
            else:
                color[i] = 'red'
        for i in last_skill_count:
            if(len(i)==1):
                val_now.append(str(i[0]))
                val_last.append('0')
                growin_up.append('100')
            else:
                val_now.append(str(i[0]))
                val_last.append(str(i[1]))
                growin_up.append(str(i[2]))
        skill_key = '*'.join(skill_key)
        skill_value = '*'.join(val_now)
        last_skill_value = '*'.join(val_last)
        growin_up = '*'.join(growin_up)
        dict_jobname = {}
        for i in total_type.objects.filter():
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
        if 'username' in request.session:
            total_dict = {
                'date_start':date_start,
                'date_end':zz[0]+'-'+zz[1],
                'skill_key':skill_key,
                'skill_value':skill_value,
                'last_skill_value':last_skill_value,
                'get_skill':"、".join(get_skill),
                'user_name':user_name,
                'get_local':get_local,
                'type_skill':type_skill,
                'growin_up':growin_up,
                'power':power,
                'count_notice':count_notice,
                'dict_jobname': dict_jobname,
                'color':color,
                "local": get_local_fun(),
                "extends_local":extends_local,
                'count_skill':count_skill,
                "extends_type":extends_type,
            }
        else:
            total_dict = {
                'date_start':date_start,
                'date_end':zz[0]+'-'+zz[1],
                'skill_key':skill_key,
                'skill_value':skill_value,
                'last_skill_value':last_skill_value,
                'get_skill':"、".join(get_skill),
                'get_local':get_local,
                'type_skill':type_skill,
                'growin_up':growin_up,
                'dict_jobname': dict_jobname,
                'color':color,
                "local": get_local_fun(),
                "extends_local":extends_local,
                "extends_type":extends_type,
                'count_skill':count_skill,
            }   
        return render(request,'search_job/trend_skill.html',total_dict)
    else:
        date_start = str(datetime.date.today().year)+'-'+'01'
        count_skill = int(request.GET.get('cer_skill',10))
        certificate_count = {}
        extends_local = request.GET.get("extends_local","")
        extends_type = request.GET.get("extends_type","")
        year_start = int(datetime.datetime.strptime(date_start,'%Y-%m').year)
        month_start = int(datetime.datetime.strptime(date_start,'%Y-%m').month)
        date_start_day = date_start+'-01'
        last_date_start = str(year_start-1)+'-'+str(month_start)+'-01'
        zz = date_end.split('-')
        date_end = zz[0]+'-'+zz[1]+'-'+str(calendar.monthrange(int(zz[0]),int(zz[1]))[1])
        last_date_end = str(int(zz[0])-1)+'-'+zz[1]+'-'+str(calendar.monthrange(int(zz[0]),int(zz[1]))[1])
        skill_count_zz =  getjob.objects.exclude(certificate = '不拘').filter(type = type_skill).values('certificate')
        for i in skill_count_zz:
            oo = i['certificate'].split('、')
            for oksd in oo:
                if(oksd in certificate_count):
                    certificate_count[oksd] +=1
                else:
                    certificate_count[oksd] =1
        certificate_count = dict(sorted( certificate_count.items(),key=lambda x:(x[1]),reverse=True))
        last_skill_count = list(certificate_count.values())[:count_skill]
        val_now = []
        val_last = []
        growin_up = []
        color = {}
        skill_key = list(certificate_count.keys())[:count_skill]
        list_skill = get_skill
        for i in skill_key:
            if(i.lower() in list_skill):
                color[i] = 'green'
            else:
                color[i] = 'red'
        for i in last_skill_count:
            val_now.append(str(i))
            val_last.append('0')
            growin_up.append('100')
        skill_key = '*'.join(skill_key)
        skill_value = '*'.join(val_now)
        last_skill_value = '*'.join(val_last)
        growin_up = '*'.join(growin_up)
        dict_jobname = {}
        for i in total_type.objects.filter():
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
        if 'username' in request.session:
            total_dict = {
                'date_start':date_start,
                'date_end':zz[0]+'-'+zz[1],
                'skill_key':skill_key,
                'skill_value':skill_value,
                'last_skill_value':last_skill_value,
                'get_skill':"、".join(get_skill),
                'user_name':user_name,
                'get_local':get_local,
                'type_skill':type_skill,
                'growin_up':growin_up,
                'power':power,
                'count_notice':count_notice,
                'dict_jobname': dict_jobname,
                'color':color,
                "local": get_local_fun(),
                "extends_local":extends_local,
                'count_skill':count_skill,
                "extends_type":extends_type,
            }
        else:
            total_dict = {
                'date_start':date_start,
                'date_end':zz[0]+'-'+zz[1],
                'skill_key':skill_key,
                'skill_value':skill_value,
                'last_skill_value':last_skill_value,
                'get_skill':"、".join(get_skill),
                'get_local':get_local,
                'type_skill':type_skill,
                'growin_up':growin_up,
                'dict_jobname': dict_jobname,
                'color':color,
                "local": get_local_fun(),
                "extends_local":extends_local,
                "extends_type":extends_type,
                'count_skill':count_skill,
            }   
        return render(request,'search_job/trend_certificate.html',total_dict)
    

    
def popular_job(request):
    get_skill = request.GET['get_skill'].lower().replace(',',"、").split("、")
    type_skill = request.GET['job']
    extends_local = request.GET.get("extends_local","")
    extends_type = request.GET.get("extends_type","")
    filter_popular = {
        'count':request.GET.get('count',1),
        "recommend":request.GET.get('recommend',2),
        'fraction':request.GET.get('fraction',3)
    }
    filter_popular = dict(sorted(filter_popular.items(), key = lambda kv:kv[1]))
    dict_jobname = {}
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
    max = page*10
    low = max -10
    popular_job =Popular_job.objects.filter().values('popular_jobid').annotate(Count('popular_jobid')).order_by('-popular_jobid__count')
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        user_good_jobid = Popular_job.objects.filter(popular_job_user_id =request.session['username']).values_list('popular_jobid_id',flat=True)
    else:
        user_good_jobid = []
    jobid_dict = {}
    for i in popular_job:
        if(i['popular_jobid'] in user_good_jobid):
            jobid_dict[i['popular_jobid']] = {'count':i['popular_jobid__count'],'recommend':'yes'}
        else:
            jobid_dict[i['popular_jobid']] = {'count':i['popular_jobid__count'],'recommend':'no'}
    get_local =request.GET.get('get_local',"")
    if(get_local != ""):
        get_local = json.loads(get_local)
        q_objects = Q()
        for k,v in get_local.items():
            for i in v:
                if( i== k):
                    q_objects |= Q(local__icontains=k)
                else:
                    q_objects |= Q(local__icontains=k+i) # 使用 |= 來建立多個OR條件
        popular_job = getjob.objects.filter(jobid__in = jobid_dict.keys() ,type = type_skill).filter(q_objects)
        get_local = json.dumps(get_local, ensure_ascii=False)
    else:
        popular_job = getjob.objects.filter(jobid__in = jobid_dict.keys(),type = type_skill)
    total_job = {}
    for i in popular_job:
        if(i.jobid in jobid_dict):
            fraction = 0
            skill_list = i.skill.lower().split('、') 
            for z in skill_list:
                if(z.lower() in get_skill):
                    fraction +=2
                elif z =='不拘' or  z =='無':
                    fraction = -100000
                else:
                    fraction -=10
            jobid_dict[i.jobid].update({"fraction":fraction})
            total_job[i] = jobid_dict[i.jobid]
    maxpage = len(total_job)
    if(maxpage%10==0):
        maxpage = maxpage//10
    else:
        maxpage = maxpage//10+1
    filter_list = list(filter_popular.keys())
    total_job =sorted(total_job.items(), key = lambda kv:(kv[1][filter_list[0]],kv[1][filter_list[1]],kv[1][filter_list[2]]),reverse=True)
    total_job = total_job[low:max]
    for i in total_type.objects.filter():
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
    if 'username' in request.session:
        total_dict = {
            'total_job':total_job,
            'dict_jobname':dict_jobname,
            'maxpage':maxpage,
            'get_skill':"、".join(get_skill),
            'type_skill':type_skill,
            'page':page,
            'get_local':get_local,
            'user_name':request.session['username'],
            'power':request.session['power'],
            'count':filter_popular['count'],
            "recommend":filter_popular['recommend'],
            'fraction':filter_popular['fraction'],
            "local": get_local_fun(),
            "extends_local":extends_local,
            "extends_type":extends_type,
            "count_notice":request.session['notice'],
        }
    else:
        total_dict = {
            'total_job':total_job,
            'dict_jobname':dict_jobname,
            'maxpage':maxpage,
            'get_skill':"、".join(get_skill),
            'type_skill':type_skill,
            'page':page,
            'get_local':get_local,
            'count':filter_popular['count'],
            "recommend":filter_popular['recommend'],
            'fraction':filter_popular['fraction'],
            "local": get_local_fun(),
            "extends_local":extends_local,
            "extends_type":extends_type,
        }
    return render(request,'search_job/popular_job.html',total_dict)

def popular_job_add(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        jobid = request.POST['jobid']
        if(Popular_job.objects.filter(popular_jobid_id = jobid,popular_job_user_id = request.session['username']).exists()):
            Popular_job.objects.filter(popular_jobid_id = jobid,popular_job_user_id = request.session['username']).delete()
            return JsonResponse({"status": True,'message':1},status=200)
        else:
            Popular_job(popular_job_user_id = request.session['username'],popular_jobid_id  = request.POST['jobid']).save()
            return JsonResponse({"status": True,'message':0},status=200)
    else:
        return JsonResponse({"status":"no-login",'message':'請您先登入才可以給予推薦'},status=200)

def update_skilltorecom(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        print(Recommend.objects.get(recom_user_name = "756685927"))
        zz = Recommend.objects.get(recom_user_name = request.session['username'])
        if("skill" in request.POST):
            zz.recom_skill = request.POST['skill']
            zz.save()
            return JsonResponse({"status": True,'message':1},status=200)
        else:
            return JsonResponse({"status": False,'message':0},status=200)
    else:
        return JsonResponse({"status":"no-login",'message':'請您先登入才可以給予推薦'},status=200)
def get_local_fun():
    area_data = [
    {
    "name":'台北市',
    "data":['中正區', '大同區', '中山區', '萬華區', '信義區', '松山區', '大安區', '南港區', '北投區', '內湖區', '士林區', '文山區'],
    "id":"Taipei"},
    {
    "name":'新北市',
    "data":['板橋區', '新莊區', '泰山區', '林口區', '淡水區', '金山區', '八里區', '萬里區', '石門區', '三芝區', '瑞芳區', '汐止區', '平溪區', '貢寮區', '雙溪區', '深坑區', '石碇區', '新店區', '坪林區', '烏來區', '中和區', '永和區', '土城區', '三峽區', '樹林區', '鶯歌區', '三重區', '蘆洲區', '五股區'],
    "id":"NewTaipeiCity",
    },
    {
    "name":'基隆市',
    "data":['仁愛區', '中正區', '信義區', '中山區', '安樂區', '暖暖區', '七堵區'],
    "id":"Keelung"
    },
    {"name":'桃園市',
    "data":['桃園區', '中壢區', '平鎮區', '八德區', '楊梅區', '蘆竹區', '龜山區', '龍潭區', '大溪區', '大園區', '觀音區', '新屋區', '復興區'],
    "id":"Taoyuan"
    },
    {"name":'新竹縣',
    "data":['竹北市', '竹東鎮', '新埔鎮', '關西鎮', '峨眉鄉', '寶山鄉', '北埔鄉', '橫山鄉', '芎林鄉', '湖口鄉', '新豐鄉', '尖石鄉', '五峰鄉'],
    "id":"Hsinchuc"},
    {"name":'新竹市',
    "data": ['東區', '北區', '香山區'],
    "id":"Hsinchui"},
    {"name":'苗栗縣',
     "data":['苗栗市', '通霄鎮', '苑裡鎮', '竹南鎮', '頭份鎮', '後龍鎮', '卓蘭鎮', '西湖鄉', '頭屋鄉', '公館鄉', '銅鑼鄉', '三義鄉', '造橋鄉', '三灣鄉', '南庄鄉', '大湖鄉', '獅潭鄉', '泰安鄉'],
     "id":"Miaoli"},
    {"name":'台中市',"data": ['中區', '東區', '南區', '西區', '北區', '北屯區', '西屯區', '南屯區', '太平區', '大里區', '霧峰區', '烏日區', '豐原區', '后里區', '東勢區', '石岡區', '新社區', '和平區', '神岡區', '潭子區', '大雅區', '大肚區', '龍井區', '沙鹿區', '梧棲區', '清水區', '大甲區', '外埔區', '大安區'],
    "id":"Taichung",
    },
    {"name":'南投縣',
    "data": [
        '南投市', '埔里鎮', '草屯鎮', '竹山鎮', '集集鎮', '名間鄉', '鹿谷鄉', '中寮鄉', '魚池鄉', '國姓鄉', '水里鄉', '信義鄉', '仁愛鄉'
    ],
    "id":"Nantou"},
    {"name":'彰化縣',
    "data": [
        '彰化市', '員林鎮', '和美鎮', '鹿港鎮', '溪湖鎮', '二林鎮', '田中鎮', '北斗鎮', '花壇鄉', '芬園鄉', '大村鄉', '永靖鄉', '伸港鄉', '線西鄉', '福興鄉', '秀水鄉', '埔心鄉', '埔鹽鄉', '大城鄉', '芳苑鄉', '竹塘鄉', '社頭鄉', '二水鄉', '田尾鄉', '埤頭鄉', '溪州鄉'
    ],
    "id":"Changhua"},
    
    {"name":'雲林縣',"data": [
        '斗六市', '斗南鎮', '虎尾鎮', '西螺鎮', '土庫鎮', '北港鎮', '莿桐鄉', '林內鄉', '古坑鄉', '大埤鄉', '崙背鄉', '二崙鄉', '麥寮鄉', '台西鄉', '東勢鄉', '褒忠鄉', '四湖鄉', '口湖鄉', '水林鄉', '元長鄉'
    ],
    'id':"Yunlin"}
    ,   
    {"name":'嘉義縣',
    "data": [
        '太保市', '朴子市', '布袋鎮', '大林鎮', '民雄鄉', '溪口鄉', '新港鄉', '六腳鄉', '東石鄉', '義竹鄉', '鹿草鄉', '水上鄉', '中埔鄉', '竹崎鄉', '梅山鄉', '番路鄉', '大埔鄉', '阿里山鄉'
    ],
    "id":"Chiayic"},
    {"name":'嘉義市',
    "data": [
        '東區', '西區'
    ],
    "id":"Chiayii"},
    {"name":'台南市',
    "data": [
        '中西區', '東區', '南區', '北區', '安平區', '安南區', '永康區', '歸仁區', '新化區', '左鎮區', '玉井區', '楠西區', '南化區', '仁德區', '關廟區', '龍崎區', '官田區', '麻豆區', '佳里區', '西港區', '七股區', '將軍區', '學甲區', '北門區', '新營區', '後壁區', '白河區', '東山區', '六甲區', '下營區', '柳營區', '鹽水區', '善化區', '大內區', '山上區', '新市區', '安定區'
    ],
    "id":"Tainan"},
    {"name":'高雄市',
    "data": [
        '楠梓區', '左營區', '鼓山區', '三民區', '鹽埕區', '前金區', '新興區', '苓雅區', '前鎮區', '小港區', '旗津區', '鳳山區', '大寮區', '鳥松區', '林園區', '仁武區', '大樹區', '大社區', '岡山區', '路竹區', '橋頭區', '梓官區', '彌陀區', '永安區', '燕巢區', '田寮區', '阿蓮區', '茄萣區', '湖內區', '旗山區', '美濃區', '內門區', '杉林區', '甲仙區', '六龜區', '茂林區', '桃源區', '那瑪夏區'
    ],
    "id":"Kaohsiung"},
    {
    "name":'屏東縣',
    "data": [
        '屏東市', '潮州鎮', '東港鎮', '恆春鎮', '萬丹鄉', '長治鄉', '麟洛鄉', '九如鄉', '里港鄉', '鹽埔鄉', '高樹鄉', '萬巒鄉', '內埔鄉', '竹田鄉', '新埤鄉', '枋寮鄉', '新園鄉', '崁頂鄉', '林邊鄉', '南州鄉', '佳冬鄉', '琉球鄉', '車城鄉', '滿州鄉', '枋山鄉', '霧台鄉', '瑪家鄉', '泰武鄉', '來義鄉', '春日鄉', '獅子鄉', '牡丹鄉', '三地門鄉'
    ],
    "id":"Pingtung"},
    {"name":'宜蘭縣',
    "data": [
        '宜蘭市', '羅東鎮', '蘇澳鎮', '頭城鎮', '礁溪鄉', '壯圍鄉', '員山鄉', '冬山鄉', '五結鄉', '三星鄉', '大同鄉', '南澳鄉'
    ],
    "id":"Yilan"},
    {"name":'花蓮縣',
    "data": [
        '花蓮市', '鳳林鎮', '玉里鎮', '新城鄉', '吉安鄉', '壽豐鄉', '秀林鄉', '光復鄉', '豐濱鄉', '瑞穗鄉', '萬榮鄉', '富里鄉', '卓溪鄉'
    ],
    "id":"Hualien"},
    {"name":'台東縣',"data": [
        '台東市', '成功鎮', '關山鎮', '長濱鄉', '海端鄉', '池上鄉', '東河鄉', '鹿野鄉', '延平鄉', '卑南鄉', '金峰鄉', '大武鄉', '達仁鄉', '綠島鄉', '蘭嶼鄉', '太麻里鄉'
    ],
    "id":"Taitung"},
    {"name":'澎湖縣',
    "data": [
        '馬公市', '湖西鄉', '白沙鄉', '西嶼鄉', '望安鄉', '七美鄉'
    ],"id":"Penghu"},
    {"name":'金門縣',
    "data": [
        '金城鎮', '金湖鎮', '金沙鎮', '金寧鄉', '烈嶼鄉', '烏坵鄉'
    ],
    "id":"golden"},
    {"name":'連江縣',"data": [
        '南竿鄉', '北竿鄉', '莒光鄉', '東引鄉'
    ],
    "id":"Lianjiang"},
    ]
    return area_data


def get_suggest():
    tit = {}
    like_counts = Like.objects.filter(like_type='like',like_date__gte=(datetime.date.today() - datetime.timedelta(weeks=1))).values('like_jobid', 'like_jobid__type','like_jobid__company','like_jobid__title','like_jobid__skill','like_jobid__local','like_jobid__salary',"like_jobid__href","like_jobid__certificate").annotate(count=Count('like_jobid')).order_by('-count')
    for i in like_counts:
        try:
            tit[i['like_jobid__type']].append(i)
        except KeyError:
            tit[i['like_jobid__type']] = [i]
    del like_counts
    title = list(tit.keys())
    for i in title:
        tit[i] = tit[i][:6]
    del title
    return tit
