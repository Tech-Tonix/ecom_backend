# Generated by Django 4.1.7 on 2023-06-07 16:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2023, 6, 7, 16, 46, 23, 807803, tzinfo=datetime.timezone.utc)),
        ),
    ]