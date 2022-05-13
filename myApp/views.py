from django.shortcuts import render
from django.http import HttpResponse

def sayHellow(request):
    return HttpResponse("<h3 style ='border-width:3px;border-style:dashed;border-color:#FFAC55;'>收到請求 Hellow!</h3>")
def definepage(request):
    return HttpResponse("<h3 style ='border-width:3px;border-style:dashed;border-color:#FFAC55;width:300px;height:400px';background-color:red>首頁</h3>")
# Create your views here.
