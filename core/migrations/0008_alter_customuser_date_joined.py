# Generated by Django 4.1.7 on 2023-06-06 16:49

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
            field=models.DateField(default=datetime.datetime(2023, 6, 6, 16, 49, 27, 388096, tzinfo=datetime.timezone.utc)),
        ),
    ]
