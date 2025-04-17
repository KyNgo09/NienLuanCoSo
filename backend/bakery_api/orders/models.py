from django.db import models
from django.utils import timezone
from customers.models import Customer
from products.models import Product

# Create your models here.
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method_choices = [
        ('Nhận tại cửa hàng', 'Nhận tại cửa hàng'),
        ('Thanh toán khi nhận hàng', 'Thanh toán khi nhận hàng'),
    ]
    payment_method = models.CharField(max_length=50, choices=payment_method_choices, default='Thanh toán khi nhận hàng')
    is_processed = models.BooleanField(default=False)
    class Meta:
        db_table = 'orders'

class OrderDetail(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = 'orderdetail'