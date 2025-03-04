from django.db import models

# Create your models here.
class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    loyalty_point = models.IntegerField(default=0)
    class Meta:
        db_table = 'customers'
