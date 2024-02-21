from django.urls import path,re_path
from . import views


urlpatterns = [
    path('search_job/',views.search_job,name='search_job'),
    path('search_job_skill/',views.search_job_skill),
    # path('session/',views.setsession,name='session_page'),
    path('',views.definepage_session,name='definepage'),
    path('search_company',views.company,name='company'),
    path('trend',views.trend_fun,name='trend'),
    path('first_ok',views.first_ok,name='first_ok'),
    path('popular_job',views.popular_job,name='popular_job'),
    path('popular_job_add',views.popular_job_add,name='popular_job_add'),
    path("update_skilltorecom",views.update_skilltorecom,name="update_skilltorecom"),
]