from django.urls import path
from . import views

urlpatterns = [
    path('',views.love,name='like'),
    path('nolike',views.nolike,name='nolike'),
    path('love/total',views.like ,name='user'),
    path('recommend/',views.recommend,name='user_recommend'),
    path('recommed/set/',views.recommend_set,name='recommend_set'),
    path('change/',views.change,name='change'),
    path('update/',views.update_user,name='update'),
    path('opinion/',views.opinion,name='opinion'),
    path('opinion/check',views.opinion_check,name='opinion_check'),
    path('like/like',views.like_like,name='like_like'),
    path('like/recommend',views.like_recommend,name='like_recommend'),
    # path('function/analysis',views.analysis,name='analysis'),
    path('manage/control_center',views.control,name='control_center'),
    path('manage/recommend_log',views.recommend_log, name='recommend_log'),
    path('notice',views.notice,name='notice'),
    path('remove',views.remove_notice,name='remove_notice'),
    path('set_notice',views.set_notice,name='set_notice'),
    path('remove_user',views.remove_user,name='remove_user'),
    path('user_great',views.user_great,name='user_great'),
    path("remove_user_data",views.remove_user_data, name='remove_user_data')
]