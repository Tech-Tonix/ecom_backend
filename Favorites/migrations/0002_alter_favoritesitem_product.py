# Generated by Django 4.1.7 on 2023-05-05 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
        ('Favorites', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritesitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.product'),
        ),
    ]
