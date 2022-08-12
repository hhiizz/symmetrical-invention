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
from django.contrib import admin
from django.urls import path
from myApp import views
from mysql_member import views as mysqlviews

urlpatterns = [
    # url , view(處理)functions
    path('',views.definepage),
    path('sing_up/',mysqlviews.sing_up),
    path('sing_in/',mysqlviews.sing_in),
    path('user-id/',mysqlviews.post_user),
    path('long-in/',mysqlviews.longin_post),
    path('sing_out/',mysqlviews.sing_out),
    path('search/<str:user_name>/',mysqlviews.like),
    path('search_job/',views.search_job),
    path('search_job/<str:user_name>',views.search_job_username),
    path('search_job_skill/',views.search_job_skill),
    path('<str:user_name>/',views.definepage_useranme),
]
