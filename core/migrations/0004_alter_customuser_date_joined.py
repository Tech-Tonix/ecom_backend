# Generated by Django 4.1.7 on 2023-05-21 15:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2023, 5, 21, 15, 19, 50, 37776, tzinfo=datetime.timezone.utc)),
        ),
    ]