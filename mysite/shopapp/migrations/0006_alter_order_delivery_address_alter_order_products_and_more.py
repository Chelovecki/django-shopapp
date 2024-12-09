# Generated by Django 4.0.6 on 2024-09-29 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopapp', '0005_alter_order_options_alter_product_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.TextField(blank=True, null=True, verbose_name='Delivery address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='products', to='shopapp.product', verbose_name='Products'),
        ),
        migrations.AlterField(
            model_name='order',
            name='promocode',
            field=models.CharField(blank=True, max_length=20, verbose_name='Promocode'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]