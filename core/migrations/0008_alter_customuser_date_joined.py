# Generated by Django 4.1.7 on 2023-05-22 15:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2023, 5, 22, 15, 7, 52, 878877, tzinfo=datetime.timezone.utc)),
        ),
    ]