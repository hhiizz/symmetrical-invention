# Generated by Django 4.1 on 2023-04-13 12:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("mysql_member", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Admin_log",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("admin_table", models.CharField(max_length=300, verbose_name="資料表")),
                ("admin_operate", models.CharField(max_length=300, verbose_name="操作類")),
                (
                    "admin_datetime",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="操作時間"
                    ),
                ),
                ("admin_state", models.BooleanField(default=True, verbose_name="操作狀態")),
                (
                    "admin_content",
                    models.CharField(default="", max_length=3000, verbose_name="詳細操作"),
                ),
                (
                    "admin_exception",
                    models.CharField(max_length=3000, null=True, verbose_name="操作例外"),
                ),
                (
                    "admin_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mysql_member.member",
                        verbose_name="帳號",
                    ),
                ),
            ],
            options={
                "verbose_name": "後台日誌",
                "verbose_name_plural": "後台日誌",
                "db_table": "admin_log",
            },
        ),
    ]
