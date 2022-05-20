from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime


def sayHello(request):
    return HttpResponse("<h3 style ='border-width:3px;border-style:dashed;border-color:#FFAC55;'>收到請求 Hellow!</h3>")
def definepage(request):
    return HttpResponse("<h3 style ='border-width:3px;border-style:dashed;border-color:#FFAC55;width:300px;height:400px';background-color:red>首頁</h3>")
def sayHello(request,username,page):
    dictw = {'username':username,
             'now':datetime.today(),
             'page':page}
    return render(request,'hello3.html',dictw)
# Create your views here.
