# Generated by Django 4.2.6 on 2023-10-16 18:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("adApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
