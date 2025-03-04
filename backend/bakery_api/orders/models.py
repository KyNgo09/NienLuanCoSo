from django.db import models
from django.utils import timezone
from customers.models import Customers
# Create your models here.
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method_choices = [
        ('Cash', 'Cash'),
        ('Credit card', 'Credit card'),
    ]
    payment_method = models.CharField(max_length=20, choices=payment_method_choices, default='Cash')
    class Meta:
        db_table = 'orders'