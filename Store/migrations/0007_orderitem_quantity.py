# Generated by Django 4.1.7 on 2023-05-22 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0006_alter_order_customer_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
