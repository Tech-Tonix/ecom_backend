# Generated by Django 4.1.7 on 2023-06-06 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Store', '0010_alter_ordersarchive_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placed_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Packed'), ('S', 'Shipped'), ('D', 'Delivered')], default='P', max_length=1)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArchivedOrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('archived_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archived_items', to='Store.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='archived_item', to='Store.product')),
            ],
        ),
        migrations.DeleteModel(
            name='OrdersArchive',
        ),
    ]
