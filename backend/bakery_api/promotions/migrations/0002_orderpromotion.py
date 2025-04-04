# Generated by Django 5.1.6 on 2025-03-30 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_orders_order'),
        ('promotions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPromotion',
            fields=[
                ('order_promotion_id', models.AutoField(primary_key=True, serialize=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='promotions.promotion')),
            ],
            options={
                'db_table': 'orderpromotion',
            },
        ),
    ]
