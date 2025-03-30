from django.db import models
from suppliers.models import Supplier

# Create your models here.
class Unit(models.Model):
    unit_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'unit'

class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)  
    class Meta:
        db_table = 'ingredient'
