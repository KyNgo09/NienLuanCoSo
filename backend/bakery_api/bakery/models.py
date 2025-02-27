from django.db import models

# Create your models here.
from django.db import models

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.BinaryField()  # Nếu lưu ảnh trong DB
    description = models.TextField()
    stock_quantity = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
