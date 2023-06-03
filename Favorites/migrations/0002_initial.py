# Generated by Django 4.1.7 on 2023-06-03 20:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Store', '0001_initial'),
        ('Favorites', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoritesitem',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favoritesitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_items', to='Store.product'),
        ),
    ]
