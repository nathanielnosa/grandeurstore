# Generated by Django 5.0.6 on 2024-05-24 10:02

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_by', models.CharField(max_length=50)),
                ('shipping_address', models.TextField()),
                ('mobile', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('subtotal', models.PositiveIntegerField()),
                ('amount', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order_status', models.CharField(choices=[('pending', 'pending'), ('complete', 'complete'), ('cancelled', 'cancelled')], max_length=50, null=True)),
                ('payment_method', models.CharField(choices=[('paystack', 'paystack'), ('transfer', 'transfer')], default='paystack', max_length=50, null=True)),
                ('payment_complete', models.BooleanField(default=False, null=True)),
                ('ref', models.CharField(max_length=255, null=True)),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stores.cart')),
            ],
        ),
    ]
