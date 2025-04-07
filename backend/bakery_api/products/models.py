from django.db import models

# Create your models here.
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'category'
    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock_quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    class Meta:
        db_table = 'product'
        
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    imageurl = models.CharField(max_length=255, db_column='imageurl')
    
    class Meta:
        db_table = 'productimages'  
        unique_together = (('product_id', 'imageurl'),)  

