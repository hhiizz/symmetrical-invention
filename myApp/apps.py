from django.apps import AppConfig


class MyappConfig(AppConfig):
    verbose_name = '爬蟲管理'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myApp'