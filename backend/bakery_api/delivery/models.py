from django.db import models
from orders.models import Order
# Create your models here.
class Delivery(models.Model):
    STATUS_CHOICES = [
        ('Preparing', 'Preparing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    delivery_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  
    delivery_datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Preparing')
    delivery_address = models.CharField(max_length=255)

    class Meta:
        db_table = 'delivery'