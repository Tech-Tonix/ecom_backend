# Generated by Django 4.1.7 on 2023-06-04 16:06

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
            field=models.DateField(default=datetime.datetime(2023, 6, 4, 16, 6, 45, 524482, tzinfo=datetime.timezone.utc)),
        ),
    ]
