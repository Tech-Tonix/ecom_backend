# Generated by Django 4.1.7 on 2023-05-02 07:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0002_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2023, 5, 2, 7, 26, 43, 374265, tzinfo=datetime.timezone.utc)),
        ),
    ]
