from email import message
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Member
import pymysql

import datetime
from .forms import NameForm
from .forms import LongForm
from django.http import HttpResponse,JsonResponse
from django import forms
# Create your views here.

def getdata(reuqest):
    getmysql = Member.objects.all()
    return render(reuqest,'index.html',locals())

def login(request):
    #指定要訪問的頁面，render的功能：講請求的頁面結果提交給客戶端
    return render(request,'long.html')
#註冊頁面
def regiter(request):
    return render(request,'demolong.html')
#定義一個函數，用來保存註冊的數據
def sing_in(request):
    return render(request,'sing_in/sing_in.html')
def sing_up(request):
    return render(request,'sing_in/sing_up.html')

def post_user(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid:
            form.is_valid()
            usernapo = dict()
            user_name =  form.cleaned_data['user_name']
            for i in user_name:
                if( not (i.isdigit() or i.isalpha())):
                    message = '用戶名只能出現大小寫英文和數字'
                    return render(request,'sing_in/sing_up.html',locals())
            pass_word =  form.cleaned_data['user_password']
            for i in pass_word:
                if( not (i.isdigit() or i.isalpha())):
                    message = '密碼只能出現大小寫英文和數字'
                    return render(request,'sing_in/sing_up.html',locals())
            if(len(user_name)>16 or len(pass_word)>16 or len(user_name)<6 or len(pass_word)<6):
                message = '帳號密碼為6~16位數'
                return render(request,'sing_in/sing_up.html',locals())
            try:
                user_name = Member.objects.get(username=user_name)
                message = '用戶名重複'
                return render(request,'sing_in/sing_up.html',locals())
            except :
                try:
                    max_id = int(Member.objects.last().id)
                except:
                    max_id = 1
                member=Member(user_id=max_id,username=user_name,password=pass_word,datetime=datetime.date.today())
                member.save()
                message = '註冊成功!'
                usernapo['user_name'] = user_name
                usernapo['user_password'] = pass_word
                return render(request,'sing_in/sing_up.html',locals())
        else:
            form = NameForm()

def longin_post(request):
    if request.method == 'POST':
        form = LongForm(request.POST)
        if form.is_valid():
            form.is_valid()
            user_name =  form.cleaned_data['user_name']
            pass_word =  form.cleaned_data['user_password']
            try:
                if(Member.objects.get(username=user_name,password=pass_word)):
                    return render(request,'heroes/index.html',locals())
                elif(Member.objects.get(username=user_name)):
                    message = '您的帳號錯誤或密碼錯誤'
                    return render(request,'sing_in/sing_in.html',locals())
            except:
                message = '您的帳號錯誤或密碼錯誤'
                return render(request,'sing_in/sing_in.html',locals())
        else:
            form = LongForm()
    # return render(request,'cover/index.html',locals())

def sing_out(request):
    return render(request,'heroes/index.html')
def like(request,user_name):
    return render(request,'cover/member_server.html',locals())


def love(request):
    return JsonResponse({'message':'success'})
