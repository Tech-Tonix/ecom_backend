# Generated by Django 4.1.7 on 2023-06-04 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Favorites', '0003_alter_favoritesitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoritesitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]