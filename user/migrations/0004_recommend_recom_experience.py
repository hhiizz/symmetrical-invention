# Generated by Django 4.1 on 2023-07-10 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_alter_recommend_recom_fraction"),
    ]

    operations = [
        migrations.AddField(
            model_name="recommend",
            name="recom_Experience",
            field=models.IntegerField(null=True),
        ),
    ]