# Generated by Django 4.1.7 on 2023-05-15 22:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2023, 5, 15, 22, 57, 0, 459954, tzinfo=datetime.timezone.utc)),
        ),
    ]
