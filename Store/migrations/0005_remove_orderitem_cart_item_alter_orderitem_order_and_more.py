# Generated by Django 4.1.7 on 2023-05-21 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0004_rename_cart_orderitem_cart_item_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='cart_item',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Store.order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='item', to='Store.product'),
        ),
    ]