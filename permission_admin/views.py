import datetime
import sys
import traceback
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job,DjangoJob,DjangoJobExecution
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from myApp.models import Popular_searches, crawler, getjob, Job_type, total_type,trend
from myApp.views import get_suggest
from mysql_member.models import Member, Popular_job
from django.core.paginator import Paginator
from django.http import HttpResponse,JsonResponse
from django.utils import timezone
from django.forms.models import model_to_dict
import pytz
from django.db.models import Q
import json
from django.db.models import Sum,Count
from permission_admin.forms import crawler_log_form, crawler_set_form, getjob_form, hot_search_form, like_form, member_admin, notice_form, opinion_form, popular_job_form, recommend_form, recommend_log_form, response_form, tesk_form, tesk_log_form, total_type_form, trend_form
from permission_admin.models import Admin_log
from user.models import Like, Notice, Opinion, Recommend, Recommend_log
import tzlocal
from django.db import connection
from django.db.models.functions import Cast
from django.db.models import DateField


def remove_job_table():
    today = datetime.date.today()
    twoweek = datetime.timedelta(weeks=2)
    deleteday = today-twoweek
    try:
        getjob.objects.filter(date__lte=deleteday).delete()
    except Exception:
        pass
    return True
def remove_notice():
    today = datetime.date.today()
    twoweek = datetime.timedelta(days=60)
    deleteday = today-twoweek
    try:
        Notice.objects.filter(Notice_date__lte=deleteday).delete()
    except Exception:
        pass
    return True

def remove_user_two_year():
    today = datetime.date.today()
    twoyear = relativedelta(years = 2)
    deletuser = today-twoyear
    try:
        Member.objects.filter(last_login__lte=deletuser).delete()
    except Exception:
        pass
    return True





scheduler = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))
scheduler.add_jobstore(DjangoJobStore(), "default")
# scheduler.add_job(remove_job_table,"cron",hour=13,minute=50,misfire_grace_time = 60,id='remove_job_table')
# scheduler.add_job(remove_notice,"cron",hour=14,minute=30,misfire_grace_time = 60,id='remove_notice')
# scheduler.add_job(remove_user_two_year,"cron",hour=14,minute=50,misfire_grace_time = 60,id='remove_user_two_year')
# register_events(scheduler)
scheduler.start()

def admin_index(request):
    if 'username' in request.session and  Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        today_last = datetime.datetime.today()- datetime.timedelta(days=1)
        today_now = datetime.datetime.today()
        range_lastday_today =[datetime.datetime(today_last.year,today_last.month,today_last.day,19,0,0,0,pytz.timezone('Asia/Taipei')),datetime.datetime(today_now.year,today_now.month,today_now.day,19,0,0,0,pytz.timezone('Asia/Taipei'))]
        x = crawler.objects.filter(crawler_date__range =range_lastday_today).values('crawler_type').annotate(Sum('crawler_total_count')).order_by('-crawler_total_count__sum') #使用聚合將crawler_log 進行統計
        key_str = ''
        val_str = ""
        for i in x:
            key_str += i['crawler_type']+'、'
            val_str += str(i['crawler_total_count__sum'])+'、'
        day_3 = (datetime.date.today()-datetime.timedelta(days=2))
        x = Member.objects.filter(datetime__gte = day_3).values('datetime').annotate(Count('datetime')).order_by('datetime')
        key_str_member = ''
        val_str_member = ""
        count = 0
        for i in range(3):
            if(len(x)==count or not day_3 == x[count]['datetime']):
                key_str_member += str(day_3)+'、'
                val_str_member += '0、'
            else:
                key_str_member += str(x[count]['datetime'])+'、'
                val_str_member += str(x[count]['datetime__count'])+'、'
                count+=1
            day_3+= datetime.timedelta(days=1)
        today = datetime.datetime.today()
        key_opinion = ''
        val_opinion = ''
        today = datetime.datetime(today.year,today.month, today.day, 0, 0, 0, 0, tzinfo=pytz.UTC)
        z = Opinion.objects.filter(opinion_date__gte = today).values('opinion_type').annotate(Count('opinion_id')).order_by('opinion_type')
        if(len(z)==0):
            key_opinion = '目前沒有資訊、'
            val_opinion = '1、'
        else:
            for i in z:
                key_opinion += i['opinion_type']+'、'
                val_opinion +=  str(i['opinion_id__count'])+'、'
        opinion_count =Opinion.objects.filter(opinion_response = None).count()
        recommend_bool = Recommend_log.objects.filter(relog_datetime__gte = today).exists()
        recommend_state = Recommend_log.objects.filter(relog_datetime__range =range_lastday_today)
        if(recommend_state.filter(relog_state =False).count()!=0):
            recommend_bool= 0
        else:
            if(recommend_state.count() != 0):
                recommend_bool= 1
            else:
                recommend_bool = 2
        crawler_104_state = crawler.objects.filter(crawler_date__range =range_lastday_today,crawler_website =104)
        selenium_count = Job_type.objects.count()
        if(crawler_104_state.exclude(crawler_state = True).exists()):
            crawler_104_state = 0
        else:
            if crawler_104_state.exclude(crawler_state =False).count()>= selenium_count:
                crawler_104_state = 1
            else:
                crawler_104_state = 2
        crawler_1111_state = crawler.objects.filter(crawler_date__range =range_lastday_today,crawler_website =1111)
        if(crawler_1111_state.exclude(crawler_state = True).exists()):
            crawler_1111_state = 0
        else:
            if crawler_1111_state.exclude(crawler_state =False).count()>= selenium_count:
                crawler_1111_state = 1
            else:
                crawler_1111_state = 2
        username = request.session['username']
        recommend_log = Recommend_log.objects.filter(relog_datetime__range =range_lastday_today,).values('relog_state').annotate(Count('relog_id'))
        key_recom = ''
        val_recom = ''
        for i in recommend_log:
            if(i['relog_state']):
                key_recom += '正常、'
            else:
                key_recom += '錯誤、'
            val_recom += str(i['relog_id__count'])+'、'
        zz = DjangoJobExecution.objects.filter(run_time__range = (datetime.datetime(today_last.year,today_last.month,today_last.day, 0, 0, 0, 0, tzinfo=pytz.timezone('Asia/Taipei')),datetime.datetime(today_now.year,today_now.month,today_now.day, 0, 0, 0, 0, tzinfo=pytz.timezone('Asia/Taipei'))))
        tesk_len = DjangoJob.objects.all().count()
        if(zz.exclude(exception__isnull= True).exists()):
            tesk_log = 0
        else:
            if len(zz.filter(exception__isnull=True)) >= tesk_len:
                tesk_log= 1
            else:
                tesk_log = 2
        dict_total ={
            'key_str':key_str[:len(key_str)-1],
            'val_str':val_str[:len(val_str)-1],
            'key_str_member':key_str_member[:len(key_str_member)-1],
            'val_str_member': val_str_member[:len(val_str_member)-1],
            'key_opinion': key_opinion[:len(key_opinion)-1],
            'val_opinion':val_opinion[:len(val_opinion)-1],
            'opinion_count':opinion_count,
            'recommend_bool':recommend_bool,
            'crawler_104_state':crawler_104_state,
            'crawler_1111_state':crawler_1111_state,
            'username':username,
            'key_recom':key_recom[:len(key_recom)-1],
            'val_recom':val_recom[:len(val_recom)-1],
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            "tesk_log":tesk_log,
        }
        return render(request,'Admin/defult.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def job_index(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword = request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        user_name = request.session['username']

        total_getjob = getjob.objects.filter()
        key_word_list = total_getjob.values_list('title',flat=True)
        if(keyword != ""):
            if(type_keyword == 'title'):
                paginator = Paginator(total_getjob.filter(title__icontains = keyword).order_by("jobid"),10)
            elif(type_keyword == "get_website_id"):
                paginator = Paginator(total_getjob.filter(get_website_id = keyword).order_by("jobid"),10)
            elif(type_keyword == "jobid"):
                paginator = Paginator(total_getjob.filter(jobid = keyword).order_by("jobid"),10)
            elif(type_keyword =="date"):
                paginator = Paginator(total_getjob.filter(date = keyword).order_by("jobid"),10)
            else:
                paginator = Paginator(total_getjob.filter(type = keyword).order_by("jobid"),10)
        else:
            paginator = Paginator(total_getjob.filter().order_by("jobid"),10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        total_content = {}
        total_content_recommend = {}
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        dict_jobname ={}
        type = total_type.objects.filter()
        for i in type:
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'dict_jobname':dict_jobname,
            'username':request.session['username'],
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            "key_word_list":key_word_list,
            "keyword":keyword,
            'type_keyword':type_keyword
        }
        return render(request,'Admin/getjob.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def job_change(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        type = request.POST['type']
        if(type == 'delete'):
            try:
                jobid = request.POST['jobid'].split('、)')
                total = getjob.objects.filter(jobid__in = jobid[:len(jobid)-1])
                count =  total.count()
                content = list(total.values('jobid',"title","company"))
                total.delete()
                admin_log_add(request.session['username'],"getjob","delete("+str(count)+")",content)
                return JsonResponse({"status": True,'message':'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"getjob",'delete',mesage)
                return JsonResponse({"status": False,'message':mesage},status=400)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def job_delete(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        try:
            jobid = request.POST['jobid'].split('、)')
            getjob.objects.filter(jobid__in = jobid).delete()
            return JsonResponse({"status": True,'message':'success'},status=200)
        except Exception as mesage:
            return JsonResponse({"status": False,'message':mesage},status=400)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def crawler_log(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        user_name = request.session['username']
        if(keyword == ""):      
            paginator = Paginator(crawler.objects.filter().order_by("-crawler_date"),10)   
        else:
            if(type_keyword== "date" ):
                keyword_hour= keyword + ' 00'
                dt = datetime.datetime.strptime(keyword_hour, '%Y-%m-%d %H')
                dt = pytz.timezone('Asia/Taipei').localize(dt)
                target_date_max = dt + datetime.timedelta(hours=24)
                target_date_min = dt
                query = crawler.objects.filter(crawler_date__range = [target_date_min,target_date_max]).order_by('-crawler_date')
                # target_date = timezone.datetime.strptime(keyword, '%Y-%m-%d').date()
                # query = crawler.objects.annotate(
                #     date=Cast('crawler_date', DateField())
                # ).filter(
                #     date__exact=target_date
                # ).extra(
                #     where=["DATE(CONVERT_TZ(crawler_date, '+00:00', '+08:00'))=%s"],
                #     params=[target_date]
                # ).order_by('-crawler_date')
                #     # 输出结果
                paginator = Paginator(query,10)
            elif(type_keyword == 'id'):
                paginator = Paginator(crawler.objects.filter(crawler_id=keyword).order_by("-crawler_date"),10)   
            elif(type_keyword =="state"):
                if(keyword =='True' or keyword =="true" or keyword == "0"):
                    keyword = True
                else:
                    keyword = False
                paginator = Paginator(crawler.objects.filter(crawler_state=keyword).order_by("-crawler_date"),10) 
            else:
                paginator = Paginator(crawler.objects.filter(crawler_type=keyword).order_by("-crawler_date"),10)   
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        total_content = {}
        total_content_recommend = {}
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        today_last = datetime.datetime.today()- datetime.timedelta(days=1 )
        today_now = datetime.datetime.today()
        range_lastday_today =[datetime.datetime(today_last.year,today_last.month,today_last.day,19,0,0,0,pytz.timezone('Asia/Taipei')),datetime.datetime(today_now.year,today_now.month,today_now.day,20,0,0,0,pytz.timezone('Asia/Taipei'))]
        if(keyword == ""):
            crawler_1111 = crawler.objects.filter(crawler_date__range = range_lastday_today,crawler_website = '1111').values('crawler_type').annotate(Sum('crawler_count')).order_by('crawler_count__sum')
            crawler_104 = crawler.objects.filter(crawler_date__range = range_lastday_today,crawler_website = '104').values('crawler_type').annotate(Sum('crawler_count')).order_by('crawler_count__sum')
        else:
            if(type_keyword== "date" ):
                keyword_hour= keyword + ' 00'
                dt = datetime.datetime.strptime(keyword_hour, '%Y-%m-%d %H')
                dt = pytz.timezone('Asia/Taipei').localize(dt)
                target_date_max = dt + datetime.timedelta(hours=24)
                target_date_min = dt
                target_date = timezone.datetime.strptime(keyword, '%Y-%m-%d').date()
                crawler_1111 =  crawler.objects.filter(crawler_date__range = [target_date_min,target_date_max],crawler_website = '1111').values('crawler_type').annotate(Sum('crawler_count')).order_by('crawler_count__sum')
                crawler_104 =  crawler.objects.filter(crawler_date__range = [target_date_min,target_date_max],crawler_website = '104').values('crawler_type').annotate(Sum('crawler_count')).order_by('crawler_count__sum')
                # crawler_1111 = crawler.objects.annotate(
                #     date=Cast('crawler_date', DateField())
                # ).filter(
                #     date__exact=target_date,crawler_website = '1111'
                # ).extra(
                #     where=["DATE(CONVERT_TZ(crawler_date, '+00:00', '+08:00'))=%s"],
                #     params=[target_date]
                # ).values('crawler_type').annotate(Sum('crawler_count')).order_by('crawler_count__sum')
                # crawler_104 = crawler.objects.annotate(
                #     date=Cast('crawler_date', DateField())
                # ).filter(
                #     date__exact=target_date,crawler_website = '104'
                # ).extra(
                #     where=["DATE(CONVERT_TZ(crawler_date, '+00:00', '+08:00'))=%s"],
                #     params=[target_date]
                # ).values('crawler_type').annotate(Sum('crawler_count')).order_by('crawler_count__sum')
            elif(type_keyword == "id"):
                crawler_1111 = crawler.objects.filter(crawler_id=keyword,crawler_website = '1111').values('crawler_type').annotate(Sum('crawler_count')).order_by('crawler_count__sum')
                crawler_104 = crawler.objects.filter(crawler_id=keyword,crawler_website = '104').values('crawler_type').annotate(Sum('crawler_count')).order_by('crawler_count__sum')
            else:
                crawler_1111 = crawler.objects.filter(crawler_type=keyword,crawler_website = '1111').values('crawler_type').annotate(Sum('crawler_count')).order_by('crawler_count__sum')
                crawler_104 = crawler.objects.filter(crawler_type=keyword,crawler_website = '104').values('crawler_type').annotate(Sum('crawler_count')).order_by('crawler_count__sum')
        crawler_1111_key = ''
        crawler_1111_value = ''
        crawler_104_key = ''
        crawler_104_value = ''
        for i in crawler_1111:
            crawler_1111_key += i['crawler_type']+'、'
            crawler_1111_value+= str(i['crawler_count__sum'])+'、'
        for i in crawler_104:
            crawler_104_key += i['crawler_type']+'、'
            crawler_104_value+= str(i['crawler_count__sum'])+'、'
        dict_jobname = {}
        type = total_type.objects.filter()
        for i in type:
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))

        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'crawler_1111_key':crawler_1111_key,
            'crawler_1111_value':crawler_1111_value,
            'crawler_104_key':crawler_104_key,
            'crawler_104_value':crawler_104_value,
            'dict_jobname':dict_jobname,
            'username':request.session['username'],
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            "keyword":keyword,
            'type_keyword':type_keyword

        }
        return render(request,'Admin/crawler_log.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def crawler_change(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        type = request.POST['type']
        if(type == 'delete'):
            try:
                crawler_id = request.POST['crawler_id'].split('、)')
                total = crawler.objects.filter(crawler_id__in = crawler_id[:len(crawler_id)-1])
                count = total.count()
                content = list(total.values())
                total.delete()
                admin_log_add(request.session['username'],"crawler","delete("+str(count)+")",content)
                return JsonResponse({"status": True,'message':'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"crawler","delete",mesage)
                return JsonResponse({"status": False,'message':str(mesage)},status=400)
        elif(type == 'update'):
            forms = crawler_log_form(request.POST)
            if(forms.is_valid()):
                try:
                    change_val ={}
                    change_val['id'] = forms.cleaned_data['id']
                    content_val = crawler.objects.get(crawler_id = forms.cleaned_data['id'])
                    input_time_utc = forms.cleaned_data['date'].astimezone(pytz.utc)
                    time_2 = content_val.crawler_date.replace(microsecond=0,second =0)
                    if(input_time_utc != time_2):
                        content_val.crawler_date = forms.cleaned_data['date']
                    content_val.crawler_type= Job_type.objects.get(type_name = forms.cleaned_data['job_type'])
                    content_val.crawler_website =forms.cleaned_data['website']
                    content_val.crawler_count =forms.cleaned_data['count']
                    content_val.crawler_state =  forms.cleaned_data['state']
                    content_val.crawler_contents = request.POST.get('content',None)
                    if(content_val.is_dirty(check_relationship=True)):
                        change_val.update(content_val.get_dirty_fields(check_relationship=True))
                        content_val.save()
                        admin_log_add(request.session['username'],"crawler","update",change_val)
                    return JsonResponse({"status": True,'message':'success'},status=200)
                except Exception as e:
                    admin_log_err(request.session['username'],"crawler","update",e)
                    return JsonResponse({"status": 'error_other',"message":str(e)},status=200)
            else:
                error = forms.errors.as_json()
                return JsonResponse({"status": "error",'message':error},status=200)
        elif(type =='add'):
            dict_total = {
                "date": timezone.now(),"id":20
            }
            dict_total['count'] = request.POST['count']
            dict_total['job_type']= request.POST['job_type']
            dict_total['state'] = request.POST['state']
            dict_total['website']= request.POST['website']
            forms = crawler_log_form(dict_total)
            if(forms.is_valid()):
                try:
                    content = crawler.objects.create(crawler_date = forms.cleaned_data['date'],crawler_type=Job_type.objects.get(type_name = forms.cleaned_data['job_type']),crawler_website =forms.cleaned_data['website'],crawler_count =forms.cleaned_data['count'],crawler_state =forms.cleaned_data['state'])
                    content.save()
                    admin_log_add(request.session['username'],"crawler","add",model_to_dict(content))
                    return JsonResponse({"status": True,'message':'success'},status=200)
                except Exception as e:
                    admin_log_err(request.session['username'],"crawler","add",e)
                    return JsonResponse({"status": 'error_other',"message":str(e)},status=200)
            else:
                error = forms.errors.as_json()
                return JsonResponse({"status": "error",'message':error},status=200)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})



def trend_log(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        if('job_type' in request.GET):
            job_type_now = request.GET['job_type']
        else:
            job_type_now = '軟體工程師'
        user_name = request.session['username']
        if(keyword !=""):
            if(type_keyword =="id"):
                paginator = Paginator(trend.objects.filter(trend_id = keyword).order_by("-trend_date"),10)
            elif(type_keyword == "date"):
                paginator = Paginator(trend.objects.filter(trend_date = keyword).order_by("-trend_date"),10)
            elif(type_keyword == "type"):
                paginator = Paginator(trend.objects.filter(trend_type = keyword).order_by("-trend_date"),10) 
            else:
                paginator = Paginator(trend.objects.filter().order_by("-trend_date"),10) 
        else:
            paginator = Paginator(trend.objects.filter().order_by("-trend_date"),10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        if('count_skill' in request.POST):
            count_skill = request.POST['count_skill']
        else:
            count_skill = 10
        year = datetime.datetime.today().year
        date_start = str(year)+'-01-'+'01'
        date_end = str(year)+'-12-'+'31'
        last_satrt =  str(year-1)+'-01-'+'01'
        last_end = str(year-1)+'-12-'+'31'
        skill_count_zz = trend.objects.filter(trend_date__range=[date_start,date_end],trend_type = job_type_now).values('trend_skill').annotate(Sum('trend_count')).order_by('-trend_count__sum')[:count_skill]
        skill_count = {}
        for i in skill_count_zz:
            skill_count[i['trend_skill']] = str(i['trend_count__sum'])
        skill_key = '*'.join(list(skill_count.keys()))
        skill_value = '*'.join(list(skill_count.values()))
        dict_jobname = {}
        type = total_type.objects.filter()
        for i in type:
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'skill_key':skill_key,
            'skill_value':skill_value,
            'dict_jobname':dict_jobname ,
            'job_type_now':job_type_now,
            'username':request.session['username'],
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            "keyword":keyword,
            "type_keyword":type_keyword,
        }
        return render(request,'Admin/trend.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})



def trend_change(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        type = request.POST['type']
        if(type == 'delete'):
            try:
                trend_id = request.POST['crawler_id'].split('、)')
                total = trend.objects.filter(trend_id__in = trend_id[:len(trend_id)-1])
                count = total.count()
                content = list(total.values())
                total.delete()
                admin_log_add(request.session['username'],"trend","delete("+str(count)+")",content)
                return JsonResponse({"status": True,'message':'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"trend","delete",mesage)
                return JsonResponse({"status": False,'message':str(mesage)},status=400)
        elif (type == 'update'):
            forms = trend_form(request.POST)
            if(forms.is_valid()):
                try:
                    change_val ={}
                    change_val['id'] =forms.cleaned_data['id']
                    content_val =  trend.objects.get(trend_id = forms.cleaned_data['id'])
                    content_val.trend_date =forms.cleaned_data['date']
                    content_val.trend_skill=forms.cleaned_data['skill']
                    content_val.trend_count = forms.cleaned_data['count']
                    content_val.trend_type = Job_type.objects.get(type_name = forms.cleaned_data['job_type'])
                    if(content_val.is_dirty(check_relationship=True)):
                        change_val.update(content_val.get_dirty_fields(check_relationship=True))
                        content_val.save()
                        admin_log_add(request.session['username'],"trend","update",change_val)
                    return JsonResponse({"status": True,'message':'success'},status=200)
                except Exception as e:
                    admin_log_err(request.session['username'],"trend","update",e)
                    return JsonResponse({"status": "error_Exception",'message':str(e)},status=200)
            else:
                error =  forms.errors.as_json()
                return JsonResponse({"status":'error','message':error},status=200)
        elif (type == 'add'):
            forms = trend_form(request.POST)
            if(forms.is_valid()):
                try:
                    content  = trend.objects.create(trend_date =forms.cleaned_data['date'],trend_skill=forms.cleaned_data['skill'],trend_count = forms.cleaned_data['count'],trend_type =Job_type.objects.get(type_name = forms.cleaned_data['job_type']))
                    content.save()
                    admin_log_add(request.session['username'],"trend","add",model_to_dict(content))
                    return JsonResponse({"status": True,'message':'success'},status=200)
                except Exception as e:
                    admin_log_err(request.session['username'],"trend","add",e)
                    return JsonResponse({"status": "error_Exception",'message':str(e)},status=200)
            else:
                error =  forms.errors.as_json()
                return JsonResponse({"status":'error','message':error},status=200)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})



def member(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        user_name = request.session['username']
        if(keyword != ""):
            if(type_keyword == "id"):
                paginator = Paginator(Member.objects.filter(user_id = keyword).order_by("-user_id"),10)
            elif(type_keyword == "user_name"):
                paginator = Paginator(Member.objects.filter(username = keyword).order_by("-user_id"),10)         
            elif(type_keyword =="date"):
                paginator = Paginator(Member.objects.filter(datetime = keyword).order_by("-user_id"),10) 
            elif(type_keyword == "email"):
                paginator = Paginator(Member.objects.filter(Email = keyword).order_by("-user_id"),10)  
            else:
                paginator = Paginator(Member.objects.filter().order_by("-user_id"),10)   
        else:
            paginator = Paginator(Member.objects.filter().order_by("-user_id"),10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        member = {}
        member['total_member'] = Member.objects.count()
        member_filter = Member.objects.filter(permissions = False)
        member['user'] =  member_filter.count()
        member['permission'] =  Member.objects.filter(permissions = True).count
        lively = datetime.date.today()-datetime.timedelta(weeks=1)
        member['lively'] = member_filter.filter(last_login__gte = lively).count
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'member':member,
            'username':request.session['username'],
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            'keyword':keyword,
            "type_keyword":type_keyword,
        }
        return render(request,'Admin/member.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def change_member(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        type = request.POST['type']
        if(type == 'delete'):
            try:
                id = request.POST['user_id'].split('、)')
                total = Member.objects.filter(user_id__in = id[:len(id)-1])
                count = total.count()
                content = list(total.values())
                total.delete()
                admin_log_add(request.session['username'],"Member","delete("+str(count)+")",content=content)
                return JsonResponse({"status": True,'message':'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"Member","delete",e)
                return JsonResponse({"status": False,'message':str(mesage)},status=400)
        elif (type == 'update'):
                member = member_admin(request.POST)
                if(member.is_valid()):
                    try:
                        print(member.cleaned_data)
                        change_val ={}
                        change_val['id'] = member.cleaned_data['id']
                        change_val['username'] = member.cleaned_data['username']
                        content_val =  Member.objects.get(username = member.cleaned_data['username'])
                        content_val.username =member.cleaned_data['username']
                        content_val.Email = member.cleaned_data['Email']
                        if(member.cleaned_data['line_userid'] == ""):
                            content_val.line_user_id = None
                        else:
                            content_val.line_user_id = member.cleaned_data['line_userid']
                        content_val.datetime = member.cleaned_data['datetime']
                        content_val.permissions=member.cleaned_data['permissions']
                        if(content_val.is_dirty()):
                            change_val.update(content_val.get_dirty_fields())
                            content_val.save()
                            admin_log_add(request.session['username'],"Member","update",change_val)
                        return JsonResponse({"status": True,'message':'success'},status=200)
                    except Exception as e:
                        admin_log_err(request.session['username'],"Member","update",e)
                        return JsonResponse({"status":"error_Exception",'message':str(e)},status=200)
                else:
                    error = member.errors.as_json()
                    return JsonResponse({"status": "error",'message':error},status=200)
        elif (type == 'add'):
            member = member_admin(request.POST)
            if(member.is_valid()):
                try:
                    max_id = Member.objects.values('user_id').order_by('user_id').last()['user_id']+1
                except:
                    max_id = 1
                try:
                    content = Member.objects.create(user_id =max_id,username = member.cleaned_data['username'],Email = member.cleaned_data['Email'],password =member.cleaned_data['password'],datetime = member.cleaned_data['datetime'],permissions=member.cleaned_data['permissions'])
                    content.save()
                    recomm = Recommend(recom_user_name= content,recom_count = 30)
                    recomm.save()
                    admin_log_add(request.session['username'],"Member","add",model_to_dict(content))
                    return JsonResponse({"status": True,'message':'success'},status=200)
                except Exception as e:
                    admin_log_err(request.session['username'],"Member","add",e)
                    return JsonResponse({"status":"error_Exception",'message':str(e)},status=200)
            else:
                error = member.errors.as_json()
                return JsonResponse({"status": "error",'message':error},status=200)

            # Member.objects.create(user_id =max_id,username = data[1],Email = data[2],password = data[3],datetime = data[4],permissions=data[6]).save()
            return JsonResponse({"status": True,'message':'success'},status=200)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def like_admin(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        user_name = request.session['username']
        if(keyword != ""):
            if(type_keyword == "date"):
                target_date = timezone.datetime.strptime(keyword, '%Y-%m-%d').date()
                # query = Like.objects.annotate(
                #     date=Cast('like_date', DateField())
                # ).filter(
                #     date__exact=target_date,
                # ).extra(
                #     where=["DATE(CONVERT_TZ(like_date, '+00:00', '+08:00'))=%s"],
                #     params=[target_date]
                # ).order_by('-id')
                query = Like.objects.filter(like_date = target_date).order_by('-id')
            elif(type_keyword == "id"):
                query =Like.objects.filter(id=keyword).order_by("-id")
            elif(type_keyword =="user_name"):
                query =Like.objects.filter(like_user_name = keyword).order_by("-id")
            elif(type_keyword =="type"):
                query =Like.objects.filter(like_type = keyword).order_by("-id")
            else:
                query =Like.objects.filter().order_by("-id")
        else:
            query =Like.objects.filter().order_by("-id")
        paginator = Paginator(query,10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        member_list = Member.objects.values_list('username',flat=True)
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'member_list':member_list,
            'username':request.session['username'],
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            'keyword':keyword,
            'type_keyword':type_keyword,
        }
        return render(request,'Admin/like.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def like_admin_chnage(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        type = request.POST['type']
        if(type == 'delete'):
            try:
                id = request.POST['id'].split('、)')
                total = Like.objects.filter(id__in = id[:len(id)-1])
                count = total.count()
                content = list(total.values())
                total.delete()
                admin_log_add(request.session['username'],"Like","delete("+str(count)+")",content=content)
                return JsonResponse({"status": True,'message':'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"Like","delete",mesage)
                return JsonResponse({"status": False,'message':str(mesage)},status=400)
        elif (type == 'update'):
            forms = like_form(request.POST)
            try:
                if(forms.is_valid()):
                    change_val ={}
                    change_val['id'] = forms.cleaned_data['id']
                    content_val =Like.objects.get(id = forms.cleaned_data['id'])
                    content_val.like_user_skill = forms.cleaned_data['skill']
                    content_val.like_type = forms.cleaned_data['like_type']
                    content_val.like_jobid = getjob.objects.get(jobid =forms.cleaned_data['jobid'])
                    content_val.like_user_name = Member.objects.get(username = forms.cleaned_data['username'])
                    content_val.like_date = forms.cleaned_data['date']
                    if(content_val.is_dirty(check_relationship=True)):
                        change_val.update(content_val.get_dirty_fields(check_relationship=True))
                        content_val.save()
                        admin_log_add(request.session['username'],"Like","update",change_val)
                    return JsonResponse({"status": True,'message':'success'},status=200)
                else:
                    error = forms.errors.as_json()
                    return JsonResponse({"status": 'error','message':error},status=200)
            except Exception as e:
                admin_log_err(request.session['username'],"Like","update",e)
                return JsonResponse({"status": 'error_Exception','message':str(e)},status=200)
        elif (type == 'add'):
            forms = like_form(request.POST)
            try:
                if(forms.is_valid()):
                    content = Like.objects.create(like_user_skill = forms.cleaned_data['skill'], like_type = forms.cleaned_data['like_type'],like_jobid = getjob.objects.get(jobid =  forms.cleaned_data['jobid']),like_user_name_id = forms.cleaned_data['username'], like_date = forms.cleaned_data['date'])
                    content.save()
                    admin_log_add(request.session['username'],"Like","add",model_to_dict(content))
                    return JsonResponse({"status": True,'message':'success'},status=200)
                else:
                    error = forms.errors.as_json()
                    return JsonResponse({"status": 'error','message':error},status=200)
            except Exception as e:
                admin_log_err(request.session['username'],"Like","add",e)
                return JsonResponse({"status": 'error_Exception','message':str(e)},status=200)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def admin_recommend_log(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        user_name = request.session['username']
        if(keyword != ""):
            if(type_keyword =="id"):
                paginator = Paginator(Recommend_log.objects.filter(relog_id =keyword).order_by("-relog_datetime"),10)
            elif(type_keyword == "date"):
                keyword_hour= keyword + ' 00'
                dt = datetime.datetime.strptime(keyword_hour, '%Y-%m-%d %H')
                dt = pytz.timezone('Asia/Taipei').localize(dt)
                target_date_max = dt + datetime.timedelta(hours=24)
                target_date_min = dt
                query = Recommend_log.objects.filter(relog_datetime__range = [target_date_min,target_date_max]).order_by('-relog_datetime')
                paginator = Paginator(query,10)
            elif(type_keyword == "user_name"):
                paginator = Paginator(Recommend_log.objects.filter(relog_user_name = keyword).order_by("-relog_datetime"),10)
            elif(type_keyword =="state"):
                if(keyword =='True' or keyword =="true" or keyword == "0"):
                    keyword = True
                else:
                    keyword = False
                paginator = Paginator(Recommend_log.objects.filter(relog_state = keyword).order_by("-relog_datetime"),10)
            else:
                paginator = Paginator(Recommend_log.objects.filter().order_by("-relog_datetime"),10)
        else:
            paginator = Paginator(Recommend_log.objects.filter().order_by("-relog_datetime"),10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        member_list = Member.objects.values_list('username',flat=True)
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'member_list':member_list,
            'username':request.session['username'],
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            "keyword":keyword,
            "type_keyword":type_keyword,
        }
        return render(request,'Admin/recommend_log.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})



def change_recommend_log(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        type = request.POST['type']
        if(type == 'delete'):
            try:
                id = request.POST['id'].split('、)')
                total = Recommend_log.objects.filter(relog_id__in = id[:len(id)-1])
                count = total.count()
                content = list(total.values())
                total.delete()
                admin_log_add(request.session['username'],"Recommend_log","delete("+str(count)+")",content=content)
                return JsonResponse({"status": True,'message':'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"Recommend_log","delete",mesage)
                return JsonResponse({"status": False,'message':str(mesage)},status=400)
        elif (type == 'update'):
            forms = recommend_log_form(request.POST)
            try:
                if(forms.is_valid()):
                    change_val ={}
                    change_val['id'] = forms.cleaned_data['id']
                    content_val = Recommend_log.objects.get(relog_id = forms.cleaned_data['id'])
                    input_time_utc = forms.cleaned_data['date'].astimezone(pytz.utc)
                    time_2 = content_val.relog_datetime.replace(microsecond=0,second =0)
                    if(input_time_utc != time_2):
                        content_val.relog_datetime = input_time_utc
                    content_val.relog_count = forms.cleaned_data['count']
                    content_val.relog_state= forms.cleaned_data['state']
                    content_val.relog_content = request.POST.get('content',None)
                    content_val.relog_user_name =  Member.objects.get(username = forms.cleaned_data['username'])
                    if(content_val.is_dirty(check_relationship=True)):
                        change_val.update(content_val.get_dirty_fields(check_relationship=True))
                        content_val.save()
                        admin_log_add(request.session['username'],"Recommend_log","update",change_val)
                    return JsonResponse({"status": True,'message':'success'},status=200)
                else:
                    error = forms.errors.as_json()
                    return JsonResponse({"status": 'error','message':error},status=200)
            except Exception as e:
                admin_log_err(request.session['username'],"Recommend_log","update",e)
                return JsonResponse({"status": 'error_Exception','message':str(e)},status=200)
        elif (type == 'add'):
            dict_total = {
                "date": timezone.now(),"id":20
            }
            dict_total['count'] = request.POST['count']
            dict_total['state'] = request.POST['state']
            dict_total['username'] = request.POST['username']
            dict_total['content'] = request.POST.get('content',None)
            forms = recommend_log_form(dict_total)
            try:
                if(forms.is_valid()):
                    content =  Recommend_log.objects.create(relog_datetime = forms.cleaned_data['date'] , relog_count = forms.cleaned_data['count'],relog_state= forms.cleaned_data['state'],relog_content =request.POST.get('content',None),relog_user_name_id = forms.cleaned_data['username'])
                    content.save()
                    admin_log_add(request.session['username'],"Recommend_log","add",model_to_dict(content))
                    return JsonResponse({"status": True,'message':'success'},status=200)
                else:
                    error = forms.errors.as_json()
                    return JsonResponse({"status": 'error','message':error},status=200)
            except Exception as e:
                admin_log_err(request.session['username'],"Recommend_log","add",e)
                return JsonResponse({"status": 'error_Exception','message':str(e)},status=200)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})





def admin_recommend(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        user_name = request.session['username']
        if(keyword != ""):
            if(type_keyword =="id"):
                paginator = Paginator(Recommend.objects.filter(id = keyword).order_by("-id"),10)
            elif(type_keyword =="user_name"):
                paginator = Paginator(Recommend.objects.filter(recom_user_name = keyword).order_by("-id"),10)
            elif(type_keyword == "type"):
                paginator = Paginator(Recommend.objects.filter(recom_job_type = keyword).order_by("-id"),10)
            else:
                paginator = Paginator(Recommend.objects.filter().order_by("-id"),10)
        else:
            paginator = Paginator(Recommend.objects.filter().order_by("-id"),10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        dict_jobname = {}
        type = total_type.objects.filter()
        for i in type:
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
        member_list = Member.objects.values_list('username',flat=True)
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'dict_jobname':dict_jobname,
            'member_list':member_list,
            'username':request.session['username'],
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            'keyword_list':Recommend.objects.values_list('recom_user_name_id',flat=True),
            'keyword':keyword,
            'type_keyword':type_keyword,
        }
        return render(request,'Admin/recommend.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def change_recommend(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        type = request.POST['type']
        if(type == 'delete'):
            try:
                id = request.POST['id'].split('、)')
                total = Recommend.objects.filter(id__in = id[:len(id)-1])
                count = total.count()
                content = list(total.values())
                total.delete()
                admin_log_add(request.session['username'],"Recommend","delete("+str(count)+")",content=content)
                return JsonResponse({"status": True,'message':'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"Recommend","delete",mesage)
                return JsonResponse({"status": False,'message':str(mesage)},status=400)
        elif (type == 'update'):
            forms =  recommend_form(request.POST)
            try:
                if(forms.is_valid()):
                    if (forms.cleaned_data['local']==""):
                        local = None
                    else:
                        local = forms.cleaned_data['local']
                    change_val ={}
                    change_val['id'] = forms.cleaned_data['id']
                    content_val = Recommend.objects.get(id = forms.cleaned_data['id'])
                    content_val.recom_user_name = Member.objects.get(username = forms.cleaned_data['username'])
                    content_val.recom_open = forms.cleaned_data['open_recommend']
                    content_val.recom_job_type = Job_type.objects.get(type_name = forms.cleaned_data['job_type'])
                    content_val.recom_skill= forms.cleaned_data['skill'].replace(',','、')
                    content_val.recom_local = local
                    content_val.recom_fraction = forms.cleaned_data['fraction']
                    content_val.recom_count = forms.cleaned_data['count']
                    content_val.recom_email_open = forms.cleaned_data['notice_Email']
                    if(content_val.is_dirty(check_relationship=True)):
                        change_val.update(content_val.get_dirty_fields(check_relationship=True))
                        content_val.save()
                        admin_log_add(request.session['username'],"Recommend","update",change_val)
                    return JsonResponse({"status": True,'message':'success'},status=200)
                else:
                    error = forms.errors.as_json()
                    return JsonResponse({"status": 'error','message':error},status=200)
            except Exception as e:
                admin_log_err(request.session['username'],"Recommend","update",e)
                return JsonResponse({"status": 'error_Exception','message':str(e)},status=200)
        elif (type == 'add'):
            forms =  recommend_form(request.POST)
            try:
                if(forms.is_valid()):
                    if (forms.cleaned_data['local']==""):
                        local = None
                    else:
                        local = forms.cleaned_data['local']
                    content = Recommend.objects.create(recom_user_name = Member.objects.get(username = forms.cleaned_data['username']),recom_open = forms.cleaned_data['open_recommend'] , recom_job_type = Job_type.objects.get(type_name = forms.cleaned_data['job_type']),recom_skill= forms.cleaned_data['skill'].replace(',','、'),recom_local = local,recom_fraction = forms.cleaned_data['fraction'],recom_count = forms.cleaned_data['count'],recom_email_open = forms.cleaned_data['notice_Email'])
                    content.save()
                    admin_log_add(request.session['username'],"Recommend","add",model_to_dict(content))
                    return JsonResponse({"status": True,'message':'success'},status=200)
                else:
                    error = forms.errors.as_json()
                    return JsonResponse({"status": 'error','message':error},status=200)
            except Exception as e:
                admin_log_err(request.session['username'],"Recommend","add",e)
                return JsonResponse({"status": 'error_Exception','message':str(e)},status=200)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def notice_admin(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        user_name = request.session['username']
        if(keyword != ""):
            if(type_keyword == "id"):
                paginator = Paginator(Notice.objects.filter(Notice_id=keyword).order_by("-Notice_date"),10)
            elif(type_keyword == "date"):
                paginator = Paginator(Notice.objects.filter(Notice_date=keyword).order_by("-Notice_date"),10)
            elif(type_keyword == "title"):
                paginator = Paginator(Notice.objects.filter(Notice_title =keyword).order_by("-Notice_date"),10)
            elif(type_keyword == "user_name"):
                paginator = Paginator(Notice.objects.filter(Notice_user = keyword).order_by("-Notice_date"),10)
            else:
                paginator = Paginator(Notice.objects.filter().order_by("-Notice_date"),10)
        else:
            paginator = Paginator(Notice.objects.filter().order_by("-Notice_date"),10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        member_list = Member.objects.values_list('username',flat=True)
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'member_list':member_list,
            'username':request.session['username'],
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            "keyword":keyword,
            "type_keyword":type_keyword,
        }
        return render(request,'Admin/notice.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def change_notice(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        type = request.POST['type']
        if(type == 'delete'):
            try:
                id = request.POST['id'].split('、)')
                total = Notice.objects.filter(Notice_id__in = id[:len(id)-1])
                count = total.count()
                content = list(total.values())
                total.delete()
                admin_log_add(request.session['username'],"Notice","delete("+str(count)+")",content=content)
                return JsonResponse({"status": True,'message':'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"Notice","delete",mesage)
                return JsonResponse({"status": False,'message':str(mesage)},status=200)
        elif (type == 'update'):
            forms =notice_form(request.POST)
            try:
                if(forms.is_valid()):
                    change_val ={}
                    change_val['id'] = forms.cleaned_data['id']
                    content_val = Notice.objects.get(Notice_id = forms.cleaned_data['id'])
                    content_val.Notice_user= Member.objects.get(username = forms.cleaned_data['username'])
                    content_val.Notice_title =forms.cleaned_data['title']
                    content_val.Notice_content = forms.cleaned_data['content']
                    content_val.Notice_date= forms.cleaned_data['date']
                    content_val.Notice_look = forms.cleaned_data['look_bool']
                    if(content_val.is_dirty(check_relationship=True)):
                        change_val.update(content_val.get_dirty_fields(check_relationship=True))
                        content_val.save()
                        admin_log_add(request.session['username'],"Notice","update",change_val)
                    return JsonResponse({"status": True,'message':'success'},status=200)
                else:
                    error = forms.errors.as_json()
                    return JsonResponse({"status": 'error','message':error},status=200)
            except Exception as e:
                admin_log_err(request.session['username'],"Notice","update",e)
                return JsonResponse({"status": 'error_Exception','message':str(e)},status=200)
        elif (type == 'add'):
            forms =notice_form(request.POST)
            try:
                if(forms.is_valid()):
                    content = Notice.objects.create(Notice_user= Member.objects.get(username = forms.cleaned_data['username']),Notice_title =forms.cleaned_data['title'] , Notice_content = forms.cleaned_data['content'],Notice_date= forms.cleaned_data['date'],Notice_look = forms.cleaned_data['look_bool'])
                    content.save()
                    admin_log_add(request.session['username'],"Notice","add",model_to_dict(content))
                    return JsonResponse({"status": True,'message':'success'},status=200)
                else:
                    error = forms.errors.as_json()
                    return JsonResponse({"status": 'error','message':error},status=200)
            except Exception as e:
                admin_log_err(request.session['username'],"Notice","add",e)
                return JsonResponse({"status": 'error_Exception','message':str(e)},status=200)
        elif(type == 'total'):
            forms =notice_form(request.POST)
            try:
                if(forms.is_valid()):
                    if(forms.cleaned_data['username']=='0'):
                        member_list = Member.objects.filter(permissions = False)
                        total_val ={"type":"普通用戶"}
                    elif(forms.cleaned_data['username']=='1'):
                        member_list = Member.objects.filter(permissions = True)
                        total_val ={"type":"管理者"}
                    else:
                        member_list = Member.objects.all()
                        total_val ={"type":"全體用戶"}
                    for i in member_list:
                        z = Notice.objects.create(Notice_user =  i,Notice_title =forms.cleaned_data['title'] , Notice_content = forms.cleaned_data['content'],Notice_date= forms.cleaned_data['date'],Notice_look = forms.cleaned_data['look_bool'])
                    z.save()
                    total_val['title'] = forms.cleaned_data['title']
                    total_val['content'] = forms.cleaned_data['content']
                    total_val['look'] = forms.cleaned_data['look_bool']
                    admin_log_add(request.session['username'],"Notice","total("+forms.cleaned_data['username']+")",total_val)
                    return JsonResponse({"status": True,'message':'success'},status=200)
                else:
                    error = forms.errors.as_json()
                    return JsonResponse({"status": 'error','message':error},status=200)
            except Exception as e:
                admin_log_err(request.session['username'],"Notice","total_"+forms.cleaned_data['username'],e)
                return JsonResponse({"status": 'error_Exception','message':str(e)},status=200)

    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})



def change_hot_search(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        type = request.POST['type']
        if(type == 'delete'):
            try:
                id = request.POST['id'].split('、)')
                total =  Popular_searches.objects.filter(Popular_id__in = id[:len(id)-1])
                count = total.count()
                content = list(total.values())
                total.delete()
                admin_log_add(request.session['username'],"Popular_searches","delete("+str(count)+")",content=content)
                return JsonResponse({"status": True,"message":'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"Popular_searches","delete",mesage)
                return JsonResponse({"status": False,"message":str(mesage)},status=400)
        elif (type == 'update'):
            forms  = hot_search_form(request.POST)
            try:
                if(forms.is_valid()):
                    change_val ={}
                    change_val['id'] = forms.cleaned_data['id']
                    content_val =Popular_searches.objects.get(Popular_id = forms.cleaned_data['id'])
                    content_val.Popular_skill= forms.cleaned_data['skill']
                    content_val.Popular_count = forms.cleaned_data['count']
                    content_val.Popular_type = Job_type.objects.get(type_name = forms.cleaned_data['job_type'])
                    if(content_val.is_dirty(check_relationship=True)):
                        change_val.update(content_val.get_dirty_fields(check_relationship=True))
                        content_val.save()
                        admin_log_add(request.session['username'],"Popular_searches","update",change_val)
                    return JsonResponse({"status": True,"message":'success'},status=200)
                else:
                    error = forms.errors.as_json()
                    return JsonResponse({"status": 'error','message':error},status=200)
            except Exception as e:
                admin_log_err(request.session['username'],"Popular_searches","update",e)
                return JsonResponse({"status": 'error_Exception','message':str(e)},status=200)
        elif (type == 'add'):
            forms  = hot_search_form(request.POST)
            try:
                if(forms.is_valid()):
                    content = Popular_searches.objects.create(Popular_skill= forms.cleaned_data['skill'],Popular_count = forms.cleaned_data['count'], Popular_type = Job_type.objects.get(type_name = forms.cleaned_data['job_type']))
                    content.save()
                    admin_log_add(request.session['username'],"Popular_searches","add",model_to_dict(content))
                    return JsonResponse({"status": True,"message":'success'},status=200)
                else:
                    error = forms.errors.as_json()
                    return JsonResponse({"status": 'error','message':error},status=200)
            except Exception as e:
                admin_log_err(request.session['username'],"Popular_searches","add",e)
                return JsonResponse({"status": 'error_Exception','message':str(e)},status=200)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})
def hot_search(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        user_name = request.session['username']
        if(keyword != ""):
            if(type_keyword =="id"):
                paginator = Paginator(Popular_searches.objects.filter(Popular_id = keyword).order_by("-Popular_count"),10)
            elif(type_keyword == "skill"):
                paginator = Paginator(Popular_searches.objects.filter(Popular_skill =keyword).order_by("-Popular_count"),10)
            else:
                paginator = Paginator(Popular_searches.objects.filter(Popular_type = keyword).order_by("-Popular_count"),10)
        else:
            paginator = Paginator(Popular_searches.objects.filter().order_by("-Popular_count"),10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        dict_jobname ={}
        type = total_type.objects.filter()
        for i in type:
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'dict_jobname':dict_jobname,
            'username':request.session['username'],
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            'keyword':keyword,
            'type_keyword':type_keyword,
        }
        return render(request,'Admin/hot_search.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def opinion_admin(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        user_name = request.session['username']
        if(keyword != ""):
            if(type_keyword == "id"):
                paginator = Paginator(Opinion.objects.filter(opinion_id =keyword).order_by("opinion_type","-opinion_response",'-opinion_date'),10)
            elif(type_keyword =="date"):
                keyword_hour= keyword + ' 00'
                dt = datetime.datetime.strptime(keyword_hour, '%Y-%m-%d %H')
                dt = pytz.timezone('Asia/Taipei').localize(dt)
                target_date_max = dt + datetime.timedelta(hours=24)
                target_date_min = dt
                paginator = Paginator(Opinion.objects.filter(opinion_date__range = [target_date_min,target_date_max]).order_by("opinion_type","-opinion_response",'-opinion_date'),10)
            elif(type_keyword =="user_name"):
                paginator = Paginator(Opinion.objects.filter(opinion_user_name = keyword).order_by("opinion_type","-opinion_response",'-opinion_date'),10)
            elif(type_keyword =="opinion_type"):
                paginator = Paginator(Opinion.objects.filter(opinion_type = keyword).order_by("opinion_type","-opinion_response",'-opinion_date'),10)
            else:
                paginator = Paginator(Opinion.objects.filter(opinion_response=keyword).order_by("opinion_type","-opinion_response",'-opinion_date'),10)
        else:
            paginator = Paginator(Opinion.objects.filter().order_by("opinion_type","-opinion_response",'-opinion_date'),10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        try:
            max_id = Opinion.objects.last().opinion_id+1
        except:
            max_id = 1
        member_list = Member.objects.values_list('username',flat=True)
        if(paginator.num_pages<page):
            page = paginator.num_pages
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'member_list':member_list,
            'username':request.session['username'],
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            "keyword":keyword,
            'type_keyword':type_keyword,
        }
        return render(request,'Admin/opinion.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def change_opinion_admin(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        type = request.POST['type']
        if(type == 'delete'):
            try:
                id = request.POST['id'].split('、)')
                total = Opinion.objects.filter(opinion_id__in = id[:len(id)-1])
                count = total.count()
                content = list(total.values())
                total.delete()
                admin_log_add(request.session['username'],"Opinion","delete("+str(count)+")",content=content)
                return JsonResponse({"status": True,'message':'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"Opinion","delete",mesage)
                return JsonResponse({"status": False,'message':str(mesage)},status=400)
        elif (type == 'update'):
            forms  = opinion_form(request.POST)
            try:
                if(forms.is_valid()):
                    if(forms.cleaned_data['response']==""):
                        change_val ={}
                        change_val['id'] = forms.cleaned_data['id']
                        content_val =Opinion.objects.get(opinion_id = forms.cleaned_data['id'])
                        input_time_utc = forms.cleaned_data['date'].astimezone(pytz.utc)
                        time_2 = content_val.opinion_date.replace(microsecond=0,second =0)
                        if(input_time_utc != time_2):
                            content_val.opinion_date= forms.cleaned_data['date']
                        content_val.opinion_user_name=Member.objects.get(username = forms.cleaned_data['username'])
                        content_val.opinion_type = forms.cleaned_data['opinion_type']
                        content_val.opinion_content= forms.cleaned_data['content']
                        if(content_val.is_dirty(check_relationship=True)):
                            change_val.update(content_val.get_dirty_fields(check_relationship=True))
                            content_val.save()
                            admin_log_add(request.session['username'],"Opinion","update",change_val)
                    else:
                        change_val ={}
                        change_val['id'] = forms.cleaned_data['id']
                        content_val = Opinion.objects.get(opinion_id = forms.cleaned_data['id'])
                        content_val.opinion_date= forms.cleaned_data['date']
                        content_val.opinion_user_name=Member.objects.get(username = forms.cleaned_data['username'])
                        content_val.opinion_type = forms.cleaned_data['opinion_type']
                        content_val.opinion_content= forms.cleaned_data['content']
                        content_val.opinion_response = Notice.objects.get( opinion_id = forms.cleaned_data['response'])
                        if(content_val.is_dirty(check_relationship=True)):
                            change_val.update(content_val.get_dirty_fields(check_relationship=True))
                            content_val.save()
                            admin_log_add(request.session['username'],"Opinion","update_response",change_val)
                    return JsonResponse({"status": True,'message':'success'},status=200)
                else:
                    error = forms.errors.as_json()
                    return JsonResponse({"status": 'error','message':error},status=200)
            except Exception as e:
                admin_log_err(request.session['username'],"Opinion","update",e)
                return JsonResponse({"status": 'error_Exception','message':str(e)},status=200)
        elif (type == 'add'):
            dict_total = {
                "date": timezone.now(),"id":20
            }
            dict_total['response']= request.POST['response']
            dict_total['opinion_type']= request.POST['opinion_type']
            dict_total['username'] = request.POST['username']
            dict_total['content']= request.POST['content']
            forms  = opinion_form(dict_total)
            try:
                if(forms.is_valid()):
                    if(dict_total['response']==""):
                        content =  Opinion.objects.create(opinion_date= forms.cleaned_data['date'],opinion_user_name=Member.objects.get(username = forms.cleaned_data['username']), opinion_type = forms.cleaned_data['opinion_type'],opinion_content= forms.cleaned_data['content'])
                        content.save()
                        admin_log_add(request.session['username'],"Opinion","add",model_to_dict(content))
                    else:
                        content =Opinion.objects.create(opinion_date= forms.cleaned_data['date'],opinion_user_name=Member.objects.get(username = forms.cleaned_data['username']), opinion_type = forms.cleaned_data['opinion_type'],opinion_content= forms.cleaned_data['content'],opinion_response = Notice.objects.get( opinion_id  = forms.cleaned_data['response']))
                        content.save()
                        admin_log_add(request.session['username'],"Opinion","add_response",model_to_dict(content))
                    return JsonResponse({"status": True,'message':'success'},status=200)
                else:
                    error = forms.errors.as_json()
                    return JsonResponse({"status": 'error','message':error},status=200)
            except Exception as e:
                admin_log_err(request.session['username'],"Opinion","add",e)
                return JsonResponse({"status": 'error_Exception','message':str(e)},status=200)
        elif (type == 'response'):
            forms  = response_form(request.POST)
            try:
                if(forms.is_valid()):
                    z = Notice.objects.create(Notice_title = forms.cleaned_data['title'],Notice_content = forms.cleaned_data['content'],Notice_date = datetime.date.today(),Notice_look = False,Notice_user = Member.objects.get(username = forms.cleaned_data['username']))
                    z.save()
                    Opinion.objects.filter(opinion_id = forms.cleaned_data['id']).update(opinion_response = z.Notice_id)
                    content_val = model_to_dict(z)
                    content_val['opinion_id'] = forms.cleaned_data['id']
                    content_val['opinion_response'] = z.Notice_id
                    admin_log_add(request.session['username'],"Opinion + Notice","response",content_val)
                    return JsonResponse({"status": True,'message':'success'},status=200)
                else:
                    error = forms.errors.as_json()
                    return JsonResponse({"status": 'error','message':error},status=200)
            except Exception as e:
                admin_log_err(request.session['username'],"Opinion","response",e)
                return JsonResponse({"status": 'error_Exception','message':str(e)},status=200)

    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def crawler_log_set(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        user_name = request.session['username']
        if(keyword !=""):
            if(type_keyword == "id"):
                paginator = Paginator(Job_type.objects.filter(job_id=keyword).order_by("-job_id"),10)
            elif(type_keyword == "type"):
                paginator = Paginator(Job_type.objects.filter(type_name=keyword).order_by("-job_id"),10)
        else:
            paginator = Paginator(Job_type.objects.filter().order_by("-job_id"),10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        dict_jobname = {}
        type = total_type.objects.filter()
        for i in type:
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'dict_jobname':dict_jobname,
            'username':request.session['username'],
            'type':type,
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            'keyword':keyword,
            'type_keyword':type_keyword,
        }
        return render(request,'Admin/crawler_log_set.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def change_crawler_log_set(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        if(request.POST['type'] == 'delete'):
            try:
                id = request.POST['id'].split('、)')
                total = Job_type.objects.filter(job_id__in = id[:len(id)-1])
                count = total.count()
                content = list(total.values())
                total.delete()
                admin_log_add(request.session['username'],"Job_type","delete("+str(count)+")",content=content)
                return JsonResponse({"status": True,'message':'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"Job_type","delete",mesage)
                return JsonResponse({"status": False,'message':str(mesage)},status=400)
        elif (request.POST['type'] == 'update'):
            forms = crawler_set_form(request.POST)
            if(forms.is_valid()):
                try:
                    change_val ={}
                    change_val['id'] = forms.cleaned_data['id']
                    content_val =Job_type.objects.get(job_id = forms.cleaned_data['id'])
                    content_val.type_name= forms.cleaned_data['job_type']
                    content_val.type_url_104= forms.cleaned_data['url_104']
                    content_val.type_url_1111 = forms.cleaned_data['url_1111']
                    content_val.total_type_name = total_type.objects.get(id=forms.cleaned_data['total_type'])
                    if(content_val.is_dirty(check_relationship=True)):
                        change_val.update(content_val.get_dirty_fields(check_relationship=True))
                        content_val.save()
                        admin_log_add(request.session['username'],"Job_type","update",change_val)
                    return JsonResponse({"status": True,'message':'success'},status=200)
                except Exception as e:
                    admin_log_err(request.session['username'],"Job_type","update",e)
                    return JsonResponse({"status": 'error_other',"message":str(e)},status=200)
            else:
                error = forms.errors.as_json()
                return JsonResponse({"status": 'error','message':error},status=200)

        elif (request.POST['type'] == 'add'):
            forms = crawler_set_form(request.POST)
            if(forms.is_valid()):
                try:
                    max_id = Job_type.objects.values_list('job_id',flat=True).order_by('-job_id')[0]+1
                except:
                    max_id = 1
                try:
                    content = Job_type.objects.create(job_id  = max_id,type_name= forms.cleaned_data['job_type'],type_url_104= forms.cleaned_data['url_104'], type_url_1111 = forms.cleaned_data['url_1111'],total_type_name = total_type.objects.get(id=forms.cleaned_data['total_type']))
                    content.save()
                    admin_log_add(request.session['username'],"Job_type","add",model_to_dict(content))
                    return JsonResponse({"status": True,'message':'success'},status=200)
                except Exception as e:
                    admin_log_err(request.session['username'],"Job_type","add",e)
                    return JsonResponse({"status": 'error_other',"message":str(e)},status=200)
            else:
                error = forms.errors.as_json()
                return JsonResponse({"status": 'error','message':error},status=200)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def opinion_response(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        page = int(request.GET.get('page',1))
        if(keyword != ""):
            if(type_keyword == "id"):
                paginator = Paginator(Opinion.objects.filter(opinion_id =keyword,opinion_response = None).order_by("-opinion_response",'-opinion_date'),10)
            elif(type_keyword =="date"):
                keyword_hour= keyword + ' 00'
                dt = datetime.datetime.strptime(keyword_hour, '%Y-%m-%d %H')
                dt = pytz.timezone('Asia/Taipei').localize(dt)
                target_date_max = dt + datetime.timedelta(hours=24)
                target_date_min = dt
                paginator = Paginator(Opinion.objects.filter(opinion_date__range = [target_date_min,target_date_max],opinion_response = None).order_by("-opinion_response",'-opinion_date'),10)
            elif(type_keyword =="user_name"):
                paginator = Paginator(Opinion.objects.filter(opinion_user_name = keyword,opinion_response = None).order_by("-opinion_response",'-opinion_date'),10)
            else:
                paginator = Paginator(Opinion.objects.filter(opinion_type = keyword,opinion_response = None).order_by("-opinion_response",'-opinion_date'),10)
        else:
            paginator = Paginator(Opinion.objects.filter(opinion_response = None).order_by('opinion_date'),10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'current_page':current_page,
            'username':request.session['username'],
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            'keyword':keyword,
            'type_keyword':type_keyword
        }

        return render(request,'Admin/opinion_response.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def popular_job(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        user_name = request.session['username']
        if(keyword != ""):
            if(type_keyword == "id"):
                paginator = Paginator(Popular_job.objects.filter(id = keyword).order_by("-popular_jobid"),10)
            elif(type_keyword == "jobid"):
                paginator = Paginator(Popular_job.objects.filter(popular_jobid= keyword).order_by("-popular_jobid"),10)
            elif(type_keyword =="user_name"):
                paginator = Paginator(Popular_job.objects.filter(popular_job_user=keyword).order_by("-popular_jobid"),10)
            else:
                paginator = Paginator(Popular_job.objects.filter().order_by("-popular_jobid"),10)
        else:
            paginator = Paginator(Popular_job.objects.filter().order_by("-popular_jobid"),10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        member_list = Member.objects.values_list('username',flat=True)
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'member_list':member_list,
            'username':request.session['username'],
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            "keyword":keyword,
            'type_keyword':type_keyword,
        }
        return render(request,'Admin/popular_job.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def popular_job_change(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        if(request.POST['type'] == 'delete'):
            try:
                id = request.POST['id'].split('、)')
                total = Popular_job.objects.filter(id__in = id[:len(id)-1])
                count = total.count()
                content = list(total.values())
                total.delete()
                admin_log_add(request.session['username'],"Popular_job","delete("+str(count)+")",content=content)
                return JsonResponse({"status": True,'message':'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"Popular_job","delete",mesage)
                return JsonResponse({"status": False,'message':str(mesage)},status=400)
        elif (request.POST['type'] == 'update'):
            forms = popular_job_form(request.POST)
            if(forms.is_valid()):
                try:
                    change_val ={}
                    change_val['id'] = forms.cleaned_data['id']
                    content_val =Popular_job.objects.get(id = forms.cleaned_data['id'])
                    content_val.popular_jobid = getjob.objects.get(jobid = forms.cleaned_data['jobid'])
                    content_val.popular_job_user = Member.objects.get(username = forms.cleaned_data['username'])
                    if(content_val.is_dirty(check_relationship=True)):
                        change_val.update(content_val.get_dirty_fields(check_relationship=True))
                        content_val.save()
                        admin_log_add(request.session['username'],"Popular_job","update",content=change_val)
                    return JsonResponse({"status": True,'message':'success'},status=200)
                except Exception as e:
                    admin_log_err(request.session['username'],"Popular_job","update",e)
                    return JsonResponse({"status": 'error_other',"message":str(e)},status=200)
            else:
                error = forms.errors.as_json()
                return JsonResponse({"status": 'error','message':error},status=200)

        elif (request.POST['type'] == 'add'):
            forms = popular_job_form(request.POST)
            if(forms.is_valid()):
                try:
                    content = Popular_job.objects.create(popular_jobid = getjob.objects.get(jobid = forms.cleaned_data['jobid']), popular_job_user = Member.objects.get(username = forms.cleaned_data['username']))
                    content.save()
                    admin_log_add(request.session['username'],"Popular_job","add",model_to_dict(content))
                    return JsonResponse({"status": True,'message':'success'},status=200)
                except Exception as e:
                    admin_log_err(request.session['username'],"Popular_job","add",e)
                    return JsonResponse({"status": 'error_other',"message":str(e)},status=200)
            else:
                error = forms.errors.as_json()
                return JsonResponse({"status": 'error','message':error},status=200)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def total_type_admin(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        if(keyword != ""):
            if(type_keyword =="id"):
                paginator = Paginator(total_type.objects.filter(id= keyword).order_by("-id"),10)
            else:
                paginator = Paginator(total_type.objects.filter(total_type_name =keyword).order_by("-id"),10)
        else:
            paginator = Paginator(total_type.objects.filter().order_by("-id"),10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'username':request.session['username'],
            "list_search":json.dumps(get_search()),
            "list_search_keys":get_search().keys(),
            "keyword":keyword,
            "type_keyword":type_keyword,
        }
        return render(request,'Admin/total_type.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def total_type_admin_change(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        if(request.POST['type'] == 'delete'):
            try:
                id = request.POST['id'].split('、)')
                total = total_type.objects.filter(id__in = id[:len(id)-1])
                count = total.count()
                content = list(total.values())
                total.delete()
                admin_log_add(request.session['username'],"total_type","delete("+str(count)+")",content=content)
                return JsonResponse({"status": True,'message':'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"total_type","delete",mesage)
                return JsonResponse({"status": 'error','message':str(mesage)},status=200)
        elif (request.POST['type'] == 'update'):
            forms = total_type_form(request.POST)
            if(forms.is_valid()):
                try:
                    change_val ={}
                    change_val['id'] = forms.cleaned_data['id']
                    content_val =total_type.objects.get(id = forms.cleaned_data['id'])
                    content_val.total_type_name = forms.cleaned_data['total_type']
                    if(content_val.is_dirty(check_relationship=True)):
                        change_val.update(content_val.get_dirty_fields(check_relationship=True))
                        content_val.save()
                        admin_log_add(request.session['username'],"total_type","update",content=change_val)
                    return JsonResponse({"status": True,'message':'success'},status=200)
                except Exception as e:
                    admin_log_err(request.session['username'],"total_type","update",e)
                    return JsonResponse({"status": 'error_other',"message":str(e)},status=200)
            else:
                error = forms.errors.as_json()
                return JsonResponse({"status": 'error','message':error},status=200)

        elif (request.POST['type'] == 'add'):
            forms = total_type_form(request.POST)
            if(forms.is_valid()):
                try:
                    content = total_type.objects.create(total_type_name = forms.cleaned_data['total_type'])
                    content.save()
                    admin_log_add(request.session['username'],"total_type","add",model_to_dict(content))
                    return JsonResponse({"status": True,'message':'success'},status=200)
                except Exception as e:
                    admin_log_err(request.session['username'],"total_type","add",e)
                    return JsonResponse({"status": 'error_other',"message":str(e)},status=200)
            else:
                error = forms.errors.as_json()
                return JsonResponse({"status": 'error','message':error},status=200)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})



def tesk(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        z = scheduler.get_jobs()
        nn= []
        for i in z:
            k = {}
            k['id'] = i.id
            k['next_run_time'] = i.next_run_time
            k['trigger'] = i.trigger.__class__.__name__.replace("Trigger","").lower()
            if(i.trigger.__class__.__name__ == "IntervalTrigger"):
                if(i.trigger.interval.seconds%108000 ==0):
                    k['time'] = str(i.trigger.interval.days)+" days"
                elif(i.trigger.interval.seconds%3600 ==0):
                    k['time'] = str(i.trigger.interval.days*24+i.trigger.interval.seconds//3600)+" hours"
                elif(i.trigger.interval.seconds%60 ==0):
                    k['time'] = str(i.trigger.interval.seconds//3600+i.trigger.interval.seconds//60)+" minutes"
                else:
                    k['time'] = str(i.trigger.interval.seconds//60+i.trigger.interval.seconds)+" seconds"
            elif(i.trigger.__class__.__name__ =="CronTrigger"):
                k['time'] =str(i.trigger.fields[5])+":"+ str(i.trigger.fields[6])
            elif(i.trigger.__class__.__name__ =="DateTrigger"):
                k['time'] =i.trigger.run_date
            nn.append(k)
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        paginator = Paginator(nn,10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'username':request.session['username'],
        }
        return render(request,'Admin/tesk.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def tesk_change(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        if(request.POST['type'] == 'delete'):
            try:
                total_tesk = []
                id = request.POST['id'].split('、)')
                for i in range(len(id)-1):
                    total_tesk.append(scheduler.get_job(job_id = id[i]))
                    scheduler.remove_job(id[i])
                admin_log_add(request.session['username'],"Djangojob","delete("+str(len(id)-1)+")",total_tesk)
                return JsonResponse({"status": True,'message':'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"Djangojob","delete",mesage)
                return JsonResponse({"status": 'error','message':str(mesage)},status=200)
        elif (request.POST['type'] == 'update'):
            forms = tesk_form(request.POST)
            if(forms.is_valid()):
                job_scheduler = scheduler.get_job(job_id = forms.cleaned_data['id'])
                try:
                    if (forms.cleaned_data['trigger']=="date"):
                        time = forms.cleaned_data['time'].replace('T',' ')+":00"
                        scheduler.reschedule_job(job_id = forms.cleaned_data['id'],trigger=forms.cleaned_data['trigger'],run_date = time)
                    elif(forms.cleaned_data['trigger']=="cron"):
                        time = str(forms.cleaned_data['time']).split(':')
                        scheduler.reschedule_job(job_id = forms.cleaned_data['id'],trigger=forms.cleaned_data['trigger'],hour=time[0],minute=time[1])
                    else:
                        time = forms.cleaned_data['time'].split(" ")
                        if(time[1]=='days'):
                            scheduler.reschedule_job(job_id = forms.cleaned_data['id'],trigger=forms.cleaned_data['trigger'],days = int(time[0]))
                        elif(time[1]=='hours'):
                            scheduler.reschedule_job(job_id = forms.cleaned_data['id'],trigger=forms.cleaned_data['trigger'],hours= int(time[0]))
                        elif(time[1]=='minutes'):
                            scheduler.reschedule_job(job_id = forms.cleaned_data['id'],trigger=forms.cleaned_data['trigger'],minutes= int(time[0]))
                        else:
                            scheduler.reschedule_job(job_id = forms.cleaned_data['id'],trigger=forms.cleaned_data['trigger'],seconds=  int(time[0]))
                    if(not forms.cleaned_data['state']):
                        scheduler.pause_job(job_id = forms.cleaned_data['id'])
                    admin_log_add(request.session['username'],"Djangojob","update",job_scheduler)
                    return JsonResponse({"status": True,'message':'success'},status=200)
                except Exception as e:
                    admin_log_err(request.session['username'],"Djangojob","update",e)
                    return JsonResponse({"status": 'error_other',"message":str(e)},status=200)
            else:
                error = forms.errors.as_json()
                return JsonResponse({"status": 'error','message':error},status=200)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def tesk_log(request):
    if Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if(keyword != ""):
            if(type_keyword =="id"):
                all_job_executions = DjangoJobExecution.objects.filter(id=keyword)
            elif(type_keyword =="job_id"):
                all_job_executions = DjangoJobExecution.objects.filter(job_id =keyword)
            elif(type_keyword =="date"):
                keyword_hour= keyword + ' 00'
                dt = datetime.datetime.strptime(keyword_hour, '%Y-%m-%d %H')
                dt = pytz.timezone('Asia/Taipei').localize(dt)
                target_date_max = dt + datetime.timedelta(hours=24)
                target_date_min = dt
                all_job_executions = DjangoJobExecution.objects.filter(run_time__range = [target_date_min,target_date_max])
            elif(type_keyword  =="exception"):
                if(keyword =='True' or keyword =="true" or keyword == "0"):
                    all_job_executions = DjangoJobExecution.objects.filter(exception = None)
                else:
                    all_job_executions = DjangoJobExecution.objects.exclude(exception = None)
            else:
                all_job_executions = DjangoJobExecution.objects.all()
        else:
            all_job_executions = DjangoJobExecution.objects.all()
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        paginator = Paginator(all_job_executions,10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'username':request.session['username'],
            "keyword":keyword,
            'type_keyword':type_keyword,
        }
        return render(request,'Admin/tesk_log.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def tesk_log_change(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username'],permissions = True).exists() :
        if(request.POST['type'] == 'delete'):
            try:
                id = request.POST['id'].split('、)')
                total = DjangoJobExecution.objects.filter(id__in = id[:len(id)-1])
                count  = total.count()
                content = list(total.values())
                total.delete()
                admin_log_add(request.session['username'],"DjangoJobExecution","delete("+str(count)+")",content=content)
                return JsonResponse({"status": True,'message':'success'},status=200)
            except Exception as mesage:
                admin_log_err(request.session['username'],"DjangoJobExecution","delete",mesage)
                return JsonResponse({"status": 'error','message':str(mesage)},status=200)
        elif (request.POST['type'] == 'update'):
            forms = tesk_log_form(request.POST)
            if(forms.is_valid()):
                try:
                    change_val ={}
                    change_val['id'] = forms.cleaned_data['id']
                    content_val =DjangoJobExecution.objects.get(id = forms.cleaned_data['id'])
                    content_val.job_id = DjangoJob.objects.get(id= forms.cleaned_data['job_id'])
                    input_time_utc = forms.cleaned_data['run_time'].astimezone(pytz.utc)
                    time_2 = content_val.run_time.replace(microsecond=0,second =0)
                    if(input_time_utc != time_2):
                        content_val.run_time = forms.cleaned_data['run_time']
                    content_val.duration = forms.cleaned_data['duration']
                    content_val.exception = request.POST.get('exception',None)
                    content_val.traceback = request.POST.get('traceback',None)
                    if(content_val.is_dirty(check_relationship=True)):
                        change_val.update(content_val.get_dirty_fields(check_relationship=True))
                        content_val.save()
                        admin_log_add(request.session['username'],"DjangoJobExecution","update",change_val)
                    return JsonResponse({"status": True,'message':'success'},status=200)
                except Exception as e:
                    admin_log_err(request.session['username'],"DjangoJobExecution","update",e)
                    return JsonResponse({"status": 'error_other',"message":str(e)},status=200)
            else:
                error = forms.errors.as_json()
                return JsonResponse({"status": 'error','message':error},status=200)

        elif (request.POST['type'] == 'add'):
            forms = tesk_log_form(request.POST)
            if(forms.is_valid()):
                try:
                    content = DjangoJobExecution.objects.create(job_id =DjangoJob.objects.get(id= forms.cleaned_data['job_id']),run_time = forms.cleaned_data['run_time'],duration = forms.cleaned_data['duration'],exception = request.POST.get('exception',None),traceback = request.POST.get('traceback',None))
                    content.save()
                    admin_log_add(request.session['username'],"DjangoJobExecution","add",model_to_dict(content))
                    return JsonResponse({"status": True,'message':'success'},status=200)
                except Exception as e:
                    admin_log_err(request.session['username'],"DjangoJobExecution","add",e)
                    return JsonResponse({"status": 'error_other',"message":str(e)},status=200)
            else:
                error = forms.errors.as_json()
                return JsonResponse({"status": 'error','message':error},status=200)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def admin_log(request):
    if Member.objects.filter(username=request.session['username'],permissions = True).exists():
        keyword =  request.GET.get('key_word_submit_2',"")
        type_keyword = request.GET.get('search_key_type',"")
        if(keyword != ""):
            if(type_keyword == "id"):
                admin_log_data = Admin_log.objects.filter(id = keyword).order_by("-id")
            elif(type_keyword =="user_name"):
                admin_log_data = Admin_log.objects.filter(admin_name = keyword).order_by("-id")
            elif(type_keyword =="table"):
                admin_log_data = Admin_log.objects.filter(admin_table = keyword).order_by("-id")
            elif(type_keyword =="operate"):
                admin_log_data = Admin_log.objects.filter(admin_operate__icontains = keyword).order_by("-id")
            elif(type_keyword =="date"):
                keyword_hour= keyword + ' 00'
                dt = datetime.datetime.strptime(keyword_hour, '%Y-%m-%d %H')
                dt = pytz.timezone('Asia/Taipei').localize(dt)
                target_date_max = dt + datetime.timedelta(hours=24)
                target_date_min = dt
                admin_log_data = Admin_log.objects.filter(admin_datetime__range =[target_date_min,target_date_max]).order_by("-id")
            elif(type_keyword =="state"):
                if(keyword =='True' or keyword =="true" or keyword == "0"):
                    keyword = True
                else:
                    keyword = False
                admin_log_data = Admin_log.objects.filter(admin_state = False).order_by("-id")
            else:
                admin_log_data = Admin_log.objects.all().order_by("-id")
        else:
            admin_log_data = Admin_log.objects.all().order_by("-id")
        if('page' in  request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        paginator = Paginator(admin_log_data,10)
        page_start_end = {}
        if(page>3):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        current_page =paginator.get_page(page)
        page_start_end['max_page'] = paginator.num_pages
        if(paginator.num_pages>6):
            if(page>paginator.num_pages-2):
                zz = paginator.num_pages-page
                page_range = range(page-(5-zz),page+zz+1)
            elif(page-2>1):
                page_range = range(page-2,page+3)
            else:
                page_range = range(1,6)
        else:
            page_range = paginator.page_range
        dict_total={
            'page':page,
            'page_start_end':page_start_end,
            'current_page':current_page,
            'page_range':page_range,
            'username':request.session['username'],
            "keyword":keyword,
            "type_keyword":type_keyword,
        }
        return render(request,'Admin/admin_log.html',dict_total)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})



def get_search():
    x = {}
    x['職缺管理'] = "/job_index/"
    x['爬蟲日誌'] = '/crawler_log/'
    x['爬蟲總類'] = "/total_type_admin/"
    x["爬蟲設定"] = "/crawler_log_set/"
    x['歷年統計'] = "/trend_log/"
    x['用戶帳密'] = "/member/"
    x['用戶喜好管理'] = "/like_admin/"
    x['用戶點讚管理'] = "/popular_job_admin/"
    x['推送日誌'] = "/admin_recommend_log/"
    x['用戶推送基本資訊'] ="/admin_recommend/"
    x['通知公告'] = "/notice_admin/"
    x['熱門收尋'] ='/hot_search/'
    x['意見箱'] = "/opinion_admin/"
    x['意見回覆'] = "/opinion_response/"
    return x


def admin_log_add(username,table,operate,content):
    Admin_log.objects.create(admin_name =Member.objects.get(username = username),admin_table=table,admin_operate =operate,admin_content = content).save


def admin_log_err(username,table,operate,err):
    err_type = err.__class__.__name__ # 取得錯誤的class 名稱
    info = err.args[0] # 取得詳細內容
    detains = traceback.format_exc() # 取得完整的tracestack
    n1, n2, n3 = sys.exc_info() #取得Call Stack
    lastCallStack =  traceback.extract_tb(n3)[-1] # 取得Call Stack 最近一筆的內容
    fn = lastCallStack [0] # 取得發生事件的檔名
    lineNum = lastCallStack[1] # 取得發生事件的行數
    funcName = lastCallStack[2] # 取得發生事件的函數名稱
    errMesg = f"FileName: {fn}, lineNum: {lineNum}, Fun: {funcName}, reason: {info}, trace:\n {traceback.format_exc()}"
    try:
        Admin_log.objects.create(admin_name = Member.objects.get(username = username),admin_table=table,admin_operate =operate,admin_state =False,admin_exception =errMesg).save()
    except:
        Admin_log.objects.create(admin_name = Member.objects.get(username = username),admin_table=table,admin_operate =operate,admin_state =False,admin_exception =f"FileName: {fn}, lineNum: {lineNum}, Fun: {funcName}"+str(err)).save()

def ssl(request):
    return render(request,'ssl/BC13B0BAC6472A6DEFE9D79EA7A709C5.txt')

def ss2(request):
    return render(request,'ssl/56A08E57440D1A82EA22F9C0386A119E.txt')