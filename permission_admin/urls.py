from django.urls import path,re_path
from . import views
urlpatterns = [
    path('admin_index/',views.admin_index,name='admin_index'),
    path('job_index/',views.job_index,name='job_index'),
    path('job_change/',views.job_change,name='job_change'),
    path('job_delete/',views.job_delete,name='job_delete'),
    path('crawler_log/',views.crawler_log,name='crawler_log'),
    path('crawler_change/',views.crawler_change,name='crawler_change'),
    path('trend_log/',views.trend_log,name='trend_log'),
    path('trend_change/',views.trend_change,name='trend_change'),
    path('member/',views.member,name='member'),
    path('change_member/',views.change_member,name='change_member'),
    path('like_admin/',views.like_admin,name='like_admin'),
    path('like_admin_chnage/',views.like_admin_chnage,name='like_admin_chnage'),
    path('admin_recommend_log/',views.admin_recommend_log,name='admin_recommend_log'),
    path('change_recommend_log/',views.change_recommend_log,name='change_recommend_log'),
    path('admin_recommend/',views.admin_recommend, name='admin_recommend'),
    path('change_recommend/',views.change_recommend,name='change_recommend'),
    path('notice_admin/',views.notice_admin,name='notice_admin'),
    path('change_notice/',views.change_notice,name='change_notice'),
    path('hot_search/',views.hot_search,name='hot_search'),
    path('change_hot_search/',views.change_hot_search,name='change_hot_search'),
    path('opinion_admin/',views.opinion_admin,name='opinion_admin'),
    path('change_opinion_admin/',views.change_opinion_admin,name='change_opinion_admin'),
    path('crawler_log_set/',views.crawler_log_set,name='crawler_log_set'),
    path('change_crawler_log_set/',views.change_crawler_log_set,name='change_crawler_log_set'),
    path('opinion_response/',views.opinion_response,name='opinion_response'),
    path('popular_job_admin/',views.popular_job,name='popular_job_admin'),
    path('popular_job_change/',views.popular_job_change,name='popular_job_change'),
    path('total_type_admin/',views.total_type_admin,name='total_type_admin'),
    path('total_type_admin_change/',views.total_type_admin_change,name='total_type_admin_change'),
    path('tesk',views.tesk,name='tesk'),
    path('tesk_change',views.tesk_change,name='tesk_change'),
    path('tesk_log',views.tesk_log,name='tesk_log'),
    path('tesk_log_change',views.tesk_log_change,name='tesk_log_change'),
    path('admin_log',views.admin_log,name="admin_log")



]