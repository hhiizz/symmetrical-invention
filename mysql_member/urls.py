from django.urls import path,re_path
from . import views
urlpatterns = [
    path('sing_up/',views.sing_up),
    # path('like/',views.like),
    path('sing_in/',views.sing_in,name='sing_in'),
    path('user-id/',views.post_user),
    path('long-in/',views.longin_post),
    path('sing_out/',views.sing_out,name='out'),
    path('test_email',views.test_email,name='test_email'),
    path('check/',views.check,name='check'),
    path('forget_password',views.forget_password,name='forget_password'),
    path('forget_get',views.forget_get,name='forget_get'),
    path('forget_check',views.forget_check,name='forget_check'),
    path('change_password',views.change_password,name='change_password'),

]