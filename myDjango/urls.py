"""myDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from cgi import test
from unittest.mock import patch

from django.contrib import admin
from django.urls import path, include,re_path
from myApp import views
from mysql_member import views as mysqlviews
from user import views
from myApp.views import definepage
from permission_admin.views import ssl, ss2

urlpatterns = [
    # url , view(處理)functions
    path('',definepage),
    path('myApp/',include('myApp.urls')),
    path('member/',include('mysql_member.urls')),
    path('user/',include('user.urls')),
    path('permission_admin/',include('permission_admin.urls')),
    path('admin/', admin.site.urls),
    path('line_bot/',include("line_bot.urls")),
    path('.well-known/pki-validation/BC13B0BAC6472A6DEFE9D79EA7A709C5.txt',ssl),
    path('.well-known/pki-validation/56A08E57440D1A82EA22F9C0386A119E.txt',ss2)
]
