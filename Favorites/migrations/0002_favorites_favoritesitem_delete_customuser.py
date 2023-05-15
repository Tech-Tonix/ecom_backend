# Generated by Django 4.1.7 on 2023-05-15 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Favorites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FavoritesItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('Favorites', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Favorites.favorites')),
            ],
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
