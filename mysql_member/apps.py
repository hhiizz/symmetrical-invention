from django.apps import AppConfig


class MysqlMemberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mysql_member'
    verbose_name='用戶系統'
