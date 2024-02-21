from django.contrib import admin

from mysql_member.models import Member
class memberaddmin(admin.ModelAdmin):
    list_display=('user_id','username','password','datetime')
admin.site.register(Member,memberaddmin)