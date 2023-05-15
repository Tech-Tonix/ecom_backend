# Generated by Django 4.1.7 on 2023-05-15 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('rating', models.PositiveIntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
