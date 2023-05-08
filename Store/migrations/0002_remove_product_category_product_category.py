# Generated by Django 4.1.7 on 2023-05-08 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Category',
        ),
        migrations.AddField(
            model_name='product',
            name='Category',
            field=models.ManyToManyField(related_name='products', to='Store.category'),
        ),
    ]
