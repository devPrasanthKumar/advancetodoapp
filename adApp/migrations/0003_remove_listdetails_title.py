# Generated by Django 4.2.6 on 2023-10-18 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("adApp", "0002_customuser_uuid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="listdetails",
            name="title",
        ),
    ]
