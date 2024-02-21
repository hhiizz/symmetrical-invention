from email import message
import email
from django.contrib.auth import authenticate
import random
from django.shortcuts import render,redirect
import re
from validate_email import validate_email
from django.contrib.auth.models import User
from myApp.models import Job_type, total_type
from myApp.views import get_suggest
from python_email.recommend_Email import recmooemd_email
from user.models import Notice, Recommend
from .models import Member
import pymysql
import datetime
from .forms import NameForm
from .forms import LongForm
from django.http import HttpResponse,JsonResponse
from django import forms
# Create your views here.





def sing_in(request):
    return render(request,'sing_in/sing_in.html')
def sing_up(request):
    return render(request,'sing_in/sing_up.html')

def post_user(request):
    if request.method == 'POST':
        user_name =  request.POST['user_name']
        password2 = request.POST['user_password2']
        email = request.POST['email']
        pass_word = request.POST['user_password']
        for i in user_name:
            if( not (i.isdigit() or i.isalpha())):
                message = '用戶名只能出現大小寫英文和數字!'
                return render(request,'sing_in/sing_up.html',locals())
        for i in pass_word:
            if( not (i.isdigit() or i.isalpha())):
                message = '密碼只能出現大小寫英文和數字!'
                return render(request,'sing_in/sing_up.html',locals())
        if(len(user_name)>16 or len(pass_word)>16 or len(user_name)<6 or len(pass_word)<6):
            message = '帳號密碼為6~16位數!'
            return render(request,'sing_in/sing_up.html',locals())
        try:
            Member.objects.get(username=user_name)
            message = '用戶名重複!'
            return render(request,'sing_in/sing_up.html',locals())
        except :
            if(password2!=pass_word):
                message = '兩次輸入的密碼不同!'
                return render(request,'sing_in/sing_up.html',locals())
            rem =r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if(re.match(rem,email)):
                if(validate_email(email)):
                    usernapo= {}
                    try:
                        Member.objects.get(Email=email)
                        message = 'email以被註冊!'
                        return render(request,'sing_in/sing_up.html',locals())
                    except:
                        request.session['username'] =user_name
                        request.session['password'] = pass_word
                        request.session['Email'] = email
                        usernapo['email'] = email
                        time = 60
                        vertical = ""
                        list = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','z','w','x','y','z']
                        for i in range(0,6):
                            vertical += random.choice(list)
                        request.session['vertical'] = vertical
                        print(request.session['vertical'],email)
                        recmooemd_email(email,vertical)
                        return render(request,'sing_in/test_email.html',locals())
                else:
                    message = 'email不可用'
                return render(request,'sing_in/text_email.html',locals())
            else:
                message = 'email格式錯誤'
                return render(request,'sing_in/sing_up.html',locals())
    else:
        form = NameForm()


def longin_post(request):
    if request.method == 'POST':
        user_name =  request.POST['user_name']
        pass_word =  request.POST['user_password']
        first = request.POST.get('first')
        tit = get_suggest()
        if(not Member.objects.filter(username=user_name).exists()):
            message = '帳號不存在或輸入錯誤!'
            return render(request,'sing_in/sing_in.html',locals())
        elif(not Member.objects.filter(username=user_name,password=pass_word).exists()):
            message = '密碼錯誤!'
            return render(request,'sing_in/sing_in.html',locals())
        else:
            request.session['username'] =user_name
            member = Member.objects.filter(username = user_name,password = pass_word , permissions = True)
            if(member.exists()):
                request.session['power'] = 'manage'
                power ='manage'
            else:
                request.session['power'] = 'user'
                power ='user'
            request.session['notice'] = Notice.objects.filter(Notice_user_id = user_name,Notice_look = False).exists()
            count_notice =request.session['notice']
            dict_jobname = {}
            for i in total_type.objects.filter():
                dict_jobname[i.total_type_name] = list(i.job_type_set.values_list('type_name',flat=True))
            Member.objects.filter(username = user_name,password = pass_word ).update(last_login= datetime.date.today())
            data_dict = {
                'count_notice':count_notice,
                'dict_jobname':dict_jobname,
                'power':power,
                'user_name':user_name,
                'pass_word':pass_word,
                'first':first
            }
            tit = get_suggest()
            return render(request,'heroes/index.html',locals())


def sing_out(request):
    request.session.flush()
    tit = get_suggest()
    return render(request,'heroes/index.html',{"tit":tit})


def test_email(request):
    if request.POST['time'] == '0':
        print(request.POST['time'])
        time = 60
        usernapo = {}
        email =  request.session['Email']
        usernapo['email'] = email
        vertical = ""
        list = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','z','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        for i in range(0,6):
            vertical += random.choice(list)
        request.session['vertical'] = vertical
        print(request.session['vertical'],"---------------------------------------驗證碼-------------------------")
        recmooemd_email(email,vertical)
        return render(request,'sing_in/test_email.html',locals())
    else:
        usernapo={}
        time = request.POST['time']
        usernapo['email'] = request.session['Email']
        return render(request,'sing_in/test_email.html',locals())



def check(request):
    usernapo={}
    usernapo['email'] = request.session['Email']
    time = request.POST['time']
    if request.POST['vertical']=="":
        message = '請填寫驗證碼'
        return render(request,'sing_in/test_email.html',locals())
    elif request.POST['vertical'].lower() == request.session['vertical']:
        usernapo = {}
        usernapo['user_name'] = request.session['username']
        usernapo['user_password'] = request.session['password']
        email = request.session['Email']
        try:
            max_id = Member.objects.values('user_id').order_by('user_id').last()['user_id']+1
        except:
            max_id = 1
        member=Member(user_id=max_id,username=usernapo['user_name'],password=request.session['password'],datetime=datetime.date.today(),Email=request.session['Email'])
        member.save()
        recomm = Recommend(recom_user_name= member)
        recomm.save()
        message = '註冊成功!'
        first = 1
        del request.session['vertical']
        del request.session['Email']
        del request.session['password']
        return render(request,'sing_in/sing_up.html',locals())
    else:
        print(request.session['vertical'])
        message = '驗證碼錯誤'
        return render(request,'sing_in/test_email.html',locals())



def forget_password(request):
    return render(request,'sing_in/forget.html')


def forget_get(request):
    if(request.POST['type'] == 'get1'):
        Email = request.POST['Email']
        if(Member.objects.filter(Email = Email).exists()):
            listmember = [0,1,2,3,4,5,6,7,8,9]
            list = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
            ver_code =  random.choice(listmember)
            vertical = str(ver_code)
            for i in range(6):
                vertical+=random.choice(list)
            vertical_code =str(ver_code)
            for i in range(1,7):
                if(i%3==0):
                    vertical_code+=chr(ord(vertical[i])+ver_code)
                elif(i%3==1):
                    vertical_code+=chr(ord(vertical[i])-ver_code)
                else:
                    vertical_code+=vertical[i]
                ver_code+=1
            recmooemd_email(Email,vertical)
            request.session['vertical'] = vertical_code
            return JsonResponse({"status": True,'message':'success'},status=200)
        else:
            return JsonResponse({"status": True,'message':'error'},status=200)
    else:
        listmember = [0,1,2,3,4,5,6,7,8,9]
        list = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        ver_code =  random.choice(listmember)
        vertical = str(ver_code)
        for i in range(6):
            vertical+=random.choice(list)
        vertical_code =str(ver_code)
        print(vertical)
        for i in range(1,7):
            if(i%3==0):
                vertical_code+=chr(ord(vertical[i])+ver_code)
            elif(i%3==1):
                vertical_code+=chr(ord(vertical[i])-ver_code)
            else:
                vertical_code+=vertical[i]
            ver_code+=1
        recmooemd_email(Email,vertical)
        request.session['vertical'] = vertical_code
        return JsonResponse({"status": True,'message':'success'},status=200)


def forget_check(request):
    vertical_code = request.session['vertical']
    user_input = request.POST['vertical']
    Email = request.POST['email']
    time = request.POST['time']
    re_code= vertical_code[0]
    re_code_int = int(re_code)
    for i in range(1,7):
        if(i%3==0):
            re_code+=chr(ord(vertical_code[i])-re_code_int)
        elif(i%3==1):
            re_code+=chr(ord(vertical_code[i])+re_code_int)
        else:
            re_code+=vertical_code[i]
        re_code_int+=1
    if(re_code == user_input):
        request.session['Email'] = Email
        return render(request,'sing_in/change_password.html')
    else:
        dict_data={
            'time':time,
            'state':'False',
            'email':Email,
        }
        return render(request,'sing_in/forget.html',dict_data)


def change_password(request):
    check_password = request.POST['check_password']
    for i in check_password:
        if( not (i.isdigit() or i.isalpha())):
            dict_data = {
                'message':0
            }
            return render(request,'sing_in/change_password.html',dict_data )
    if(len(check_password)>16 or len(check_password)<6 ):
        dict_data = {
            'message':1
        }
        return render(request,'sing_in/change_password.html',dict_data)
    dict_data = {
        'message':2
    }
    Email = request.session['Email']
    Member.objects.filter(Email = Email).update(password = check_password)
    return render(request,'sing_in/change_password.html',dict_data)



