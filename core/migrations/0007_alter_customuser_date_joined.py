# Generated by Django 4.1.7 on 2023-05-11 10:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_customuser_groups_customuser_user_permissions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2023, 5, 11, 10, 8, 30, 242224, tzinfo=datetime.timezone.utc)),
        ),
    ]
