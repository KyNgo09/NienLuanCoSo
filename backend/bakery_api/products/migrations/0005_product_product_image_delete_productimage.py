# Generated by Django 5.1.6 on 2025-03-04 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_product_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
