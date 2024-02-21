
import datetime
import email
from email import message
from fractions import Fraction
from hashlib import new
from itertools import count
from select import select
from urllib import request
from django.utils import timezone
from django.shortcuts import render
from django.core.paginator import Paginator
from validate_email import validate_email
from django.http import HttpResponse,JsonResponse

from myApp.models import Job_type, getjob, total_type
from myApp.views import get_suggest
from mysql_member.models import Member, Popular_job
from django.db.models import Sum,Count
import pytz
from .models import Like, Opinion, Recommend, Recommend_log,Notice
# Create your views here.
def love(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        if(request.method=='POST'):
            user= request.session['username']
            jobid = request.POST['jobid']
            skill = request.POST['user_skill']
            user = Member.objects.get(username = user)
            certificate_user = request.POST.get('certificate_user',None)
            if(Like.objects.filter(like_user_name = user).count()<500):
                x = Like(like_user_name=user,like_jobid_id=jobid,like_user_skill=skill,like_certificate = certificate_user)
                x.save()
                return JsonResponse({"status":"true",'message':'success'},status=200)
            else:
                return JsonResponse({"status":"error",'message':'您的資料超過500，請去刪除資料'},status=200)
    else:
        return JsonResponse({"status":"no-login",'message':'請您先登入才可以加入我的最愛'},status=200)
def nolike(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists():
        if(request.method=='POST'):
            if not 'jobid' in request.POST:
                type = request.POST['type']
                user= request.session['username']
                if(type=='total'):
                    x = Like.objects.filter(like_user_name=user)
                else:
                    x = Like.objects.filter(like_user_name=user,like_type=type)
            else:
                type = request.POST['type']
                user= request.session['username']
                jobid = request.POST['jobid']
                x = Like.objects.get(like_user_name=user,like_jobid_id=jobid,like_type=type)
            x.delete()
            return JsonResponse({'message':'success'})
    else:
        return JsonResponse({"status":"no-login",'message':'請您先登入才可以加入我的最愛'},status=200)
def like(request):  
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        user_name =request.session['username']
        like_type =  request.GET.get('like_type','全部')
        page = int(request.GET.get('page',1))
        power =  request.session['power']
        county = request.GET.get('county',"")
        district =  request.GET.get('district',"")
        x = getlike_recommend(user_name,'total',like_type,county.replace("臺","台"),district)
        count_notice =request.session['notice']
        paginator = Paginator(x[0],10)
        page_start_end = {}
        if(page>4):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        count =  paginator.count
        current_page =paginator.get_page(page)
        total_content = []
        total_content_recommend = []
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
        for i in total_type.objects.filter():
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
        dictto={
            'dict_total_like':current_page,
            'user_name':user_name,
            'like_type':like_type,
            'power':power,
            'count_notice':count_notice,
            'current_page':current_page,
            'page':page,
            'page_range':page_range,
            'count':x[1],
            "max_count":x[2],
            "page_start_end":page_start_end,
            'dict_jobname':dict_jobname,
            'county':county,
            'district':district,
        }
        return render(request,'member/user_love.html',dictto)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def recommend(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists():
        user_name =request.session['username']
        recommend = Recommend.objects.get(recom_user_name=user_name)
        user = recommend.recom_user_name.username
        open = recommend.recom_open
        if(open):
            open = 'true'
        else:
            open= 'false'
        certificate_select = recommend.recom_cer_boo
        if(certificate_select):
            certificate_select = 'true'
        else:
            certificate_select= 'false'
        count = recommend.recom_count
        user_certificate = recommend.recom_certificate
        count_notice =request.session['notice']
        skill = recommend.recom_skill
        power =  request.session['power']
        dict_jobname = {}
        Experience = recommend.recom_Experience
        fraction = recommend.recom_fraction
        type_skill = recommend.recom_job_type_id
        email = recommend.recom_email_open
        line_bot = recommend.recom_line_bot
        local = recommend.recom_local
        type = total_type.objects.filter()
        for i in type:
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
        if(count!='30' and count!='60' and count!='90' and count !='max' and count !='0'):
            user_count = count
            count= 'other'
        return render(request,'member/user_recommend.html',locals())
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def recommend_set(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        if(request.method=='POST'):
            user_name =request.session['username']
            open = request.POST['openrecommend']
            skill = request.POST.get('recommend_skill',"").replace(',',"、")
            fraction = request.POST.get('recommend_fraction',None)
            count = request.POST.get('recommend_count',"0")
            job_type = request.POST.get('recommend_job_type',None)
            email = request.POST.get('recommend_email',False)
            local = request.POST.get("recom_local",None)
            line_bot = request.POST.get('recommend_line_bot',False)
            recommend_cer_boo = request.POST.get('recommend_cer_boo',"False")
            power =  request.session['power']
            user_name = Member.objects.get(username=user_name)
            count_notice =request.session['notice']
            Experience = request.POST.get('Experience',None)
            user_certificate = request.POST.get('user_certificate',"")
            update_recommend = Recommend.objects.get(recom_user_name=user_name)
            if(Experience == "Experience_select"):
                update_recommend.recom_Experience = request.POST.get('Exper_year',0)
            else:
                update_recommend.recom_Experience = Experience
            if(open=='true'):
                update_recommend.recom_open = True
            else:
                update_recommend.recom_open = False
            if(count=="other"):
                user_count = request.POST.get('recommend_count_other',"0")
                if(int(user_count)>=500):
                    update_recommend.recom_count = "max"
                else:
                    update_recommend.recom_count =  user_count
            else:
                update_recommend.recom_count = count
            if(recommend_cer_boo == "true"):
                update_recommend.recom_cer_boo = True
                update_recommend.recom_certificate = user_certificate
            else:
                update_recommend.recom_cer_boo = False
            update_recommend.recom_skill = skill
            update_recommend.recom_fraction = fraction
            update_recommend.recom_job_type = Job_type.objects.get(type_name = job_type)
            if(line_bot=='true'):
                update_recommend.recom_line_bot = True
                line_bot = True
            else:
                update_recommend.recom_line_bot = False
                line_bot = False
            if(email=='true'):
                update_recommend.recom_email_open = True
                email = True
            else:
                update_recommend.recom_email_open = False
                email = False
            update_recommend.recom_local = local
            update_recommend.save()
            user_name = user_name.username
            return JsonResponse({"status": True,'message':'success'},status=200)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def change(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        user_name = request.session['username']
        email = Member.objects.get(username=user_name).Email
        power =  request.session['power']
        count_notice =request.session['notice']
        return render(request,'member/change_member.html',locals())
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def update_user(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        user_name = request.session['username']
        try:
            password =request.POST['old_password']
        except:
            password=""
        try:
            new_password = request.POST['new_password']
        except:
            new_password=""
        email = request.POST['Email']
        count_notice =request.session['notice']
        power =  request.session['power']
        if(email==Member.objects.get(username=user_name).Email and password=='' and new_password==''):
            message = '您沒有要修改的資料'
            return render(request,'member/change_member.html',locals())
        if(len(Member.objects.filter(username=user_name,password=password))==1 or password==""):
            if not new_password=='' or  not password=='' :
                for i in new_password:
                    if( not (i.isdigit() or i.isalpha())):
                        message = '新密碼只能出現大小寫英文和數字'
                        return render(request,'member/change_member.html',locals())
                if(len(new_password)>16 or len(new_password)<6):
                    message = '新密碼為6~16位數'
                    return render(request,'member/change_member.html',locals())
                Member.objects.filter(username=user_name).update(password=new_password)
            if  email != Member.objects.get(username=user_name).Email:
                if(not validate_email(email_address=email)):
                    message = 'email不可用'
                    return render(request,'member/change_member.html',locals())
                elif(len(Member.objects.filter(Email=email))==1):
                    message = 'email 已被註冊'
                    return render(request,'member/change_member.html',locals())
                Member.objects.filter(username=user_name).update(Email = email)
            message ='更新完畢!，請重新登入'
            del password
            del new_password
            request.session.flush()
            return render(request,'member/change_member.html',locals())
        else:
            message = '舊密碼錯誤'
            return render(request,'member/change_member.html',locals())
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def opinion(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        user_name = request.session['username']
        count_notice =request.session['notice']
        power =  request.session['power']
        return render(request,'member/opinion.html',locals())
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def opinion_check(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        user_name = request.session['username']
        type = request.POST.get('opinion_type',"")
        power =  request.session['power']
        count_notice =request.session['notice']
        content = request.POST.get('s_question',"")
        img = request.FILES.get('opinion_img',None)
        if(len(content)<=5):
            message = 0
            return render(request,'member/opinion.html',locals())
        try:
            if(img!=None):
                opinion =  Opinion(opinion_user_name_id = user_name,opinion_type = type, opinion_content=content,opinion_img = img)
            else:
                opinion =  Opinion(opinion_user_name_id = user_name,opinion_type = type, opinion_content=content)
            opinion.save()
            message = 1
            return render(request,'member/opinion.html',locals())
        except Exception:
            message = 2
            return render(request,'member/opinion.html',locals())
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def like_like(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        user_name =request.session['username']
        count_notice =request.session['notice']
        try:
            like_type =  request.GET['like_type']
        except:
            like_type = '全部'
        if( 'page' in request.GET):
            page = int(request.GET['page'])
        else:
            page = 1
        power =  request.session['power']
        county = request.GET.get('county',"")
        district =  request.GET.get('district',"")
        x = getlike_recommend(user_name,'like',like_type,county.replace("臺","台"),district)
        paginator = Paginator(x[0],10)
        page_start_end = {}
        if(page>4):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        count =  paginator.count
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
        power =  request.session['power']
        dict_jobname = {}
        for i in total_type.objects.filter():
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))

        dictto={
            'dict_total_like':current_page,
            'user_name':user_name,
            'count':x[1],
            "max_count":x[2],
            'like_type':like_type,
            'count_notice':count_notice,
            'current_page':current_page,
            'page':page,
            'page_range':page_range,
            "page_start_end":page_start_end,
            'power':power,
            'dict_jobname':dict_jobname,
            'county':county,
            'district':district
        }
        return render(request,'member/user_love_like.html',dictto)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})



def like_recommend(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        user_name =request.session['username']
        try:
            like_type =  request.GET['like_type']
        except:
            like_type = '全部'
        page = int(request.GET.get('page',1))
        county = request.GET.get("county","")
        district =  request.GET.get('district',"")
        x = getlike_recommend(user_name,'recommend',like_type,county.replace("臺",'台'),district)
        count_notice =request.session['notice']
        power =  request.session['power']

        paginator = Paginator(x[0],10)
        page_start_end = {}
        if(page>4):
            page_start_end ['start'] = True
        else:
            page_start_end ['start'] = False
        if(page<paginator.num_pages-3):
            page_start_end['end'] = True
        else:
            page_start_end['end'] = False
        count =  paginator.count
        current_page =paginator.get_page(page)
        total_content = {}
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
        power =  request.session['power']
        dict_jobname = {}
        for i in total_type.objects.filter():
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
        dictto={
            'dict_total_recommend':current_page,
            'user_name':user_name,
            'now':'recmooend',
            'like_type':like_type,
            'count_notice':count_notice,
            'current_page':current_page,
            'page':page,
            'page_range':page_range,
            'count':x[1],
            'max_count':x[2],
            "page_start_end":page_start_end,
            'power':power,
            'dict_jobname':dict_jobname,
            'county':county,
            'district':district
        }
        return render(request,'member/user_love_recommend.html',dictto)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})




def getlike_recommend(user_name,type,like_type,county,district):
    dictjob={}
    recommend_job={}
    skill_now = Like.objects.filter(like_user_name=user_name)
    local_now = county+district
    for i in range(0,len(skill_now)):
        if(county == "" and district =="") or (district == "") or (local_now == skill_now[i].like_jobid.local):
            fraction = 0
            certificate_fraction= 0
            job =skill_now[i]
            user_skill = skill_now[i].like_user_skill.lower().split("、")
            user_certificate = ""
            if(skill_now[i].like_certificate != None):
                user_certificate = skill_now[i].like_certificate.upper().split("、")
            job_skill = job.like_jobid.skill.split("、")
            certificate_job = job.like_jobid.certificate.split("、")
            for x in job_skill:
                if(x.lower() in user_skill):
                    fraction +=1
                elif x =='不拘' or x =='無':
                    fraction = -100000
                else:
                    fraction -=20
            if(certificate_job != ['']):
                for certif in certificate_job:
                    if(not certif.upper() in user_certificate):
                        certificate_fraction-=10
                    else:
                        certificate_fraction+=2
                if(certificate_fraction == len(certificate_job)*-10):
                    certificate_fraction = -float('Inf')
            else:
                certificate_fraction = -float('Inf')
            if(type=='total'):
                dictjob[job] = [fraction,certificate_fraction]
            elif(type=='like'):
                if(skill_now[i].like_type=='like'):
                    dictjob[job] = [fraction,certificate_fraction]
            else:
                if(skill_now[i].like_type=='recommend'):
                    recommend_job[job] = [fraction,certificate_fraction]
        else:
            continue
        # elif(district == ""):
        #     if(county in  skill_now[i].like_jobid.local):
        #         fraction = 0
        #         job =skill_now[i]
        #         user_skill = skill_now[i].like_user_skill.lower().split("、")
        #         job_skill = job.like_jobid.skill.split("、")
        #         certificate_job = job.like_jobid.certificate.split("、")
        #     for x in job_skill:
        #         if(x.lower() in user_skill):
        #             fraction +=1
        #         elif x =='不拘' or x =='無':
        #             fraction = -100000
        #         else:
        #             fraction -=20
        #     if(certificate_job != ['']):
        #         for certif in certificate_job:
        #             if(not certif.upper() in user_certificate):
        #                 certificate_fraction-=10
        #             else:
        #                 certificate_fraction+=2
        #         if(certificate_fraction == len(certificate_job)*-10):
        #             certificate_fraction = -float('Inf')
        #     else:
        #         certificate_fraction = -float('Inf')
        #         if(type=='total'):
        #             dictjob[job] = fraction
        #         elif(type=='like'):
        #             if(skill_now[i].like_type=='like'):
        #                 dictjob[job] = fraction
        #         else:
        #             if(skill_now[i].like_type=='recommend'):
        #                 recommend_job[job] = fraction
        # else:
        #     local_now = county+district
        #     if(local_now == skill_now[i].like_jobid.local):
        #         fraction = 0
        #         job =skill_now[i]
        #         user_skill = skill_now[i].like_user_skill.lower().split("、")
        #         job_skill = job.like_jobid.skill.split("、")
        #         for x in job_skill:
        #             if(x.lower() in user_skill):
        #                 fraction +=1
        #             elif x =='不拘' or x =='無':
        #                 fraction = -100000
        #             else:
        #                 fraction -=20
        #         if(type=='total'):
        #             dictjob[job] = fraction
        #         elif(type=='like'):
        #             if(skill_now[i].like_type=='like'):
        #                 dictjob[job] = fraction
        #         else:
        #             if(skill_now[i].like_type=='recommend'):
        #                 recommend_job[job] = fraction

    if(type=='total'):
        dictjob = dict(sorted(dictjob.items(),key=lambda y:(y[1][1],y[1][0],len(y[0].like_user_skill.split("、"))),reverse=True))
        key = list(dictjob.keys())
        dict_total_like= []
        if(like_type=='全部'):
            for i in key:
                dict_total_like.append(i)
            return [dict_total_like,len(dict_total_like),500]
        else:
            remove_count = 0
            for i in key:
                if(i.like_jobid.type_id==like_type):
                    dict_total_like.append(i)
                else:
                    remove_count +=1
            return [dict_total_like,len(dict_total_like),500- remove_count]

    elif(type=='like'):
        dictjob = dict(sorted(dictjob.items(),key=lambda y:(y[1][1],y[1][0],len(y[0].like_user_skill.split("、"))),reverse=True))
        dict_total_like=[]
        key = list(dictjob.keys())
        if(like_type=='全部'):
            for i in key:
                dict_total_like.append(i)
            return [dict_total_like,len(dict_total_like),500-len(skill_now)+len(key)]
        else:
            remove_count = 0
            for i in key:
                if(i.like_jobid.type_id==like_type):
                    dict_total_like.append(i)
                else:
                    remove_count+=1
            return [dict_total_like,len(dict_total_like),500-len(skill_now)+len(key)-remove_count]
    else:
        recommend_job = dict(sorted(recommend_job.items(),key=lambda y:(y[1][1],y[1][0],len(y[0].like_user_skill.split("、"))),reverse=True))
        key = list(recommend_job.keys())
        dict_total_recommend=[]
        if(like_type=='全部'):
            for i in key:
                dict_total_recommend.append(i)
            return [dict_total_recommend,len(dict_total_recommend),500-len(skill_now)+len(key)]
        else:
            remove_count = 0
            dict_total_recommend=[]
            for i in key:
                if(i.like_jobid.type_id==like_type):
                    dict_total_recommend.append(i)
                else:
                    remove_count+=1
            return [dict_total_recommend,len(dict_total_recommend),500-len(skill_now)+len(key)-remove_count]



def control(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        user_name =request.session['username']
        try:
            like_type =  request.GET['like_type']
        except:
            like_type = '全部'
        power =  request.session['power']
        x = getlike_recommend(user_name,'total',like_type,"","")
        total_content = x[0]
        count_notice =request.session['notice']
        dictto={
            'dict_total_like':total_content,
            'user_name':user_name,
            'like_type':like_type,
            'power':power,
            'count_notice':count_notice
        }
        return render(request,'member/control_center.html',dictto)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def recommend_log(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        dict_totoal = {}
        user_name =request.session['username']
        try:
            like_type =  request.GET['like_type']
        except:
            like_type = '全部'
        total_recommend ={}
        recommend_log =Recommend_log.objects.filter(relog_user_name = user_name).order_by("-relog_datetime").values()
        recommend_log2 =Recommend.objects.filter(recom_user_name = user_name).values()
        count_notice =request.session['notice']
        today_recommend_count = {}
        last_day = datetime.datetime.now()-datetime.timedelta(days=2)
        today = datetime.datetime.now()
        count = Recommend_log.objects.filter(relog_user_name= user_name,relog_datetime__range=[datetime.datetime(last_day.year, last_day.month, last_day.day, tzinfo=pytz.UTC),datetime.datetime(today.year,today.month,today.day+1, tzinfo=pytz.UTC)]).values('relog_datetime','relog_count')
        last_day1 = datetime.datetime.now()-datetime.timedelta(days=1)
        for i in range(2,-1,-1):
            today_recommend_count [(datetime.datetime.now()-datetime.timedelta(days=i)).strftime('%Y/%m/%d')] = '0'
        for i in count:
            if( i['relog_datetime'].strftime('%Y/%m/%d') in today_recommend_count):
                today_recommend_count[i['relog_datetime'].strftime('%Y/%m/%d')] = str(int(today_recommend_count[i['relog_datetime'].strftime('%Y/%m/%d')]) + i['relog_count'])
        recommend_count_key = '*'.join(list(today_recommend_count.keys()))
        recommend_count_value = '*'.join(list(today_recommend_count.values()))
        total_recommend[recommend_log]= recommend_log2
        y =Like.objects.filter(like_user_name=user_name,like_date = datetime.datetime.today()-datetime.timedelta(days=1),like_type='recommend')
        dict_analysis ={}
        for i in y:
            job_skill = i.like_jobid.skill.split("、")
            for x in job_skill:
                if x =='不拘' or x == "無":
                    pass
                else:
                    try:
                        dict_analysis[x.lower()]+=1
                    except:
                        dict_analysis[x.lower()] =1
        dict_analysis = dict(sorted(dict_analysis.items(),key=lambda y:y[1],reverse=True))
        analysis_keys = list(dict_analysis.keys())[:6]
        analysis_values = str(list(dict_analysis.values())[:6]).replace('[','').replace(']','')
        analysis_keys = "*".join(analysis_keys)
        power =  request.session['power']
        dict_totoal = {
            'user_name':user_name,
            'total_recommend':total_recommend,
            'recommend_log':recommend_log,
            'recommend_count_key':recommend_count_key,
            'recommend_count_value':recommend_count_value,
            'analysis_keys':analysis_keys,
            'analysis_values':analysis_values,
            'power':power,
            'count_notice':count_notice,
        }
        return render(request,'member/recommend_log.html',dict_totoal)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})



def notice(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists():
        date_dict = {}
        user_name =request.session['username']
        notice = Notice.objects.filter(Notice_user_id = user_name).order_by('-Notice_date')
        not_look_count = notice.filter(Notice_look = False).count()
        power =  request.session['power']
        count_notice =request.session['notice']
        for i in notice:
            try:
                date_dict[i.Notice_date] = date_dict[i.Notice_date] + [i]
            except:
                date_dict[i.Notice_date] = [i]
        return render(request,'member/Notice.html',locals())
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def remove_notice(request):
    if(request.method=='POST'):
        if('total' in  request.POST ):
            user= request.session['username']
            x = Notice.objects.filter(Notice_user_id=user)
        else:
            id = request.POST['id']
            x = Notice.objects.get(Notice_id = id)
        x.delete()
        return JsonResponse({'message':'success'})


def set_notice(request):
    user_name = request.session['username']
    Notice.objects.filter(Notice_user_id=user_name).update(Notice_look = True)
    request.session['notice'] = False
    return JsonResponse({'message':'success'})


def remove_user(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists():
        user_name = request.session['username']
        Member.objects.get(username = request.session['username']).delete()
        request.session.flush()
        return JsonResponse({"status": True,'message':'success'},status=200)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})

def user_great(request):
    if 'username' in request.session and Member.objects.filter(username=request.session['username']).exists() :
        page = int(request.GET.get('page',1))
        skill_great = request.GET.get('skill_great',"").lower().replace(',',"、").split('、')
        open_skill = request.GET.get('open_skill',None)
        type_job = request.GET.get('job',"全部")
        dict_jobname = {}
        for i in total_type.objects.filter():
            dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
        jobid = Popular_job.objects.filter(popular_job_user =request.session['username'])
        if(open_skill != "open"):
            jobid_new = []
            if(type_job != "全部"):
                for i in jobid:
                    if(i.popular_jobid.type_id ==type_job ):
                        jobid_new.append(i.popular_jobid)
                popular_job =Popular_job.objects.filter(popular_jobid__in = jobid_new).values('popular_jobid').annotate(Count('popular_jobid')).order_by('-popular_jobid__count')
            else:
                popular_job =Popular_job.objects.filter(popular_jobid__in = jobid.values_list('popular_jobid',flat=True)).values('popular_jobid').annotate(Count('popular_jobid')).order_by('-popular_jobid__count')
            paginator = Paginator(popular_job,10)
            page_start_end = {}
            if(page>4):
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
            popular_job = current_page
            total_job = {}
            jobid_dict = {}
            for i in popular_job:
                jobid_dict[i['popular_jobid']] = {'count':i['popular_jobid__count']}
            popular_job = getjob.objects.filter(jobid__in = jobid_dict.keys())
            for i in popular_job:
                total_job[i] = jobid_dict[i.jobid]
            total_job =sorted(total_job.items(), key = lambda kv:(kv[1]['count']),reverse=True)
            total_dict = {
            'total_job':total_job,
            'page_range':page_range,
            "page_start_end":page_start_end,
            'page':page,
            'user_name':request.session['username'],
            'power':request.session['power'],
            'dict_jobname':dict_jobname,
            'type_job':type_job,
            "open_skill":1,
            'skill_great':"、".join(skill_great),
            }
        else:
            jobid_new = []
            if(type_job != "全部"):
                for i in jobid:
                    if(i.popular_jobid.type_id ==type_job ):
                        jobid_new.append(i.popular_jobid)
                popular_job =Popular_job.objects.filter(popular_jobid__in = jobid_new)
            else:
                popular_job =Popular_job.objects.filter(popular_jobid__in = jobid.values_list('popular_jobid',flat=True))
            total_job = {}
            jobid_dict = {}
            dict_skill = {}
            popular_job_count =Popular_job.objects.filter(popular_jobid__in = jobid.values_list('popular_jobid',flat=True)).values('popular_jobid').annotate(Count('popular_jobid'))
            jobid_dict = {}
            for i in popular_job_count:
                jobid_dict[i['popular_jobid']] =i['popular_jobid__count']
            for i in popular_job:
                skill_list = i.popular_jobid.skill.split('、')
                fraction = 0
                for z in skill_list:
                    if(z.lower() in skill_great):
                        fraction +=2
                    elif z =='不拘' or  z =='無':
                        fraction = -100000
                    else:
                        fraction -=10
                total_job[i.popular_jobid] ={'fraction':fraction,"count":jobid_dict[i.popular_jobid_id]}
            total_job =sorted(total_job.items(), key = lambda kv:(kv[1]['fraction'],kv[1]['count']),reverse=True)
            paginator = Paginator(total_job,10)
            page_start_end = {}
            if(page>4):
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
            total_dict = {
                'total_job':current_page,
                'page_range':page_range,
                "page_start_end":page_start_end,
                'page':page,
                'user_name':request.session['username'],
                'power':request.session['power'],
                'dict_jobname':dict_jobname,
                'type_job':type_job,
                'dict_skill':dict_skill,
                'skill_great':"、".join(skill_great),
                "open_skill":0,
            }
        return render(request,'member/user_great.html',total_dict)
    else:
        tit = get_suggest()
        request.session.flush()
        return render(request,'heroes/index.html',{"tit":tit})


def remove_user_data(request):
    try:
        id = request.POST.get('id','').split('-')
        like_type = request.POST.get('type','').split('-')
        for i in range(len(id)-1):
            Like.objects.filter(like_user_name = request.session['username'],like_jobid_id = id[i],like_type = like_type[i]).delete()
        return JsonResponse({"status": True,'message':'success'},status=200)
    except:
        return JsonResponse({"status": "error",'message':'資料錯誤請您稍後在嘗試!'},status=200)

def get_recommend_skill(user_name):
    recommend_job = {}
    skill_now = Like.objects.filter(like_user_name=user_name,like_type = 'recommend')
    for i in range(0,len(skill_now)):
        fraction = 0
        job =skill_now[i]
        user_skill = skill_now[i].like_user_skill.lower().split("、")
        job_skill = job.like_jobid.skill.split("、")
        for x in job_skill:
            if(x.lower() in user_skill):
                fraction +=1
            elif x =='不拘' or x =='無':
                fraction = -100000
            else:
                fraction -=20
        recommend_job[job] = fraction
    recommend_job = dict(sorted(recommend_job.items(),key=lambda y:(y[1]),reverse=True))
    return recommend_job