# Generated by Django 4.1.7 on 2023-05-18 20:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2023, 5, 18, 20, 56, 25, 772776, tzinfo=datetime.timezone.utc)),
        ),
    ]