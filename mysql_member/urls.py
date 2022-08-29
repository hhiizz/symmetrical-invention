from django.urls import path,re_path
from . import views
urlpatterns = [
    path('',views.love,name='like'),
    path('sing_up/',views.sing_up),
    path('like/',views.like),
    path('sing_in/',views.sing_in),
    path('user-id/',views.post_user),
    path('long-in/',views.longin_post),
    path('sing_out/',views.sing_out),
    path('search/<str:user_name>/',views.like),
]