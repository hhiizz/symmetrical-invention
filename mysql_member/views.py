from email import message
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Member
import pymysql

import datetime
from .forms import NameForm
from .forms import LongForm
from django.http import HttpResponse
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
            pass_word =  form.cleaned_data['user_password']
            try:
                user_name = Member.objects.get(username=user_name)
                message = '用戶名重複'
                return render(request,'sing_in/sing_up.html',locals())
            except :
                member=Member(username=user_name,password=pass_word,datetime=datetime.date.today())
                member.save()
                message = '註冊成功!'
                usernapo['user_name'] = user_name
                usernapo['user_password'] = pass_word
                return render(request,'sing_in/sing_in.html',locals())
        else:
            form = NameForm()
    return render(request, 'sing_in/sing_up.html', {'form': form})

def longin_post(request):
    if request.method == 'POST':
        form = LongForm(request.POST)
        if form.is_valid():
            form.is_valid()
            user_name =  form.cleaned_data['user_name']
            pass_word =  form.cleaned_data['user_password']
            message = '沒有此帳號'
            try:
                if(Member.objects.get(username=user_name)):
                    message = '密碼錯誤'
                    if(Member.objects.get(username=user_name,password=pass_word)):
                        message ="登入成功!"
                return render(request,'cover/index.html',locals())
            except:
                return render(request,'sing_in/sing_up.html',locals())
        else:
            form = LongForm()
    # return render(request,'cover/index.html',locals())

def sing_out(request):
    return render(request,'cover/index.html')
