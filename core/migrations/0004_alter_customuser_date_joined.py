# Generated by Django 4.1.7 on 2023-06-05 09:50

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
            field=models.DateField(default=datetime.datetime(2023, 6, 5, 9, 50, 31, 611248, tzinfo=datetime.timezone.utc)),
        ),
    ]
