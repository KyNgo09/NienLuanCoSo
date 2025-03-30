from django.db import models

# Create your models here.
class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    class Meta:
        db_table = 'supplier'