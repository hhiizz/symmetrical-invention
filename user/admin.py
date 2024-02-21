from django.contrib import admin

from user.models import Like, Recommend, Recommend_log

# Register your models here.
class likeadmin(admin.ModelAdmin):
    list_display=('like_user_name','like_jobid','like_user_skill','like_type')
class recommendadmin(admin.ModelAdmin):
    list_display=('recom_user_name','recom_open','recom_job_type','recom_skill','recom_fraction','recom_count','recom_email_open')
class recommend_logadmin(admin.ModelAdmin):
    list_display=('relog_id','relog_user_name','relog_datetime','relog_count','relog_state')
admin.site.register(Like,likeadmin)
admin.site.register(Recommend,recommendadmin)
admin.site.register(Recommend_log,recommend_logadmin)