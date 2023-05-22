# Generated by Django 4.1.7 on 2023-05-22 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0007_orderitem_quantity'),
        ('Favorites', '0003_remove_favoritesitem_quantity_favorites_customer_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favoritesitem',
            old_name='Favorites',
            new_name='favorites',
        ),
        migrations.AlterField(
            model_name='favoritesitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_items', to='Store.product'),
        ),
    ]
