# Generated by Django 4.1.7 on 2023-06-06 13:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2023, 6, 6, 13, 57, 1, 367961, tzinfo=datetime.timezone.utc)),
        ),
    ]
