# Generated by Django 4.1 on 2023-06-05 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_recommend_recom_line_bot"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recommend",
            name="recom_fraction",
            field=models.CharField(
                default="max", max_length=300, null=True, verbose_name="推送篩選標準"
            ),
        ),
    ]
