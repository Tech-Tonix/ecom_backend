# Generated by Django 4.1.7 on 2023-06-07 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reviews', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='image',
        ),
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='review',
            name='title',
        ),
    ]