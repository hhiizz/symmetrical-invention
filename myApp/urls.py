from django.urls import path,re_path
from . import views


urlpatterns = [
    path('search_job/',views.search_job),
    path('search_job/<str:user_name>',views.search_job_username),
    path('search_job_skill/',views.search_job_skill),
    path('<str:user_name>/',views.definepage_useranme),
]