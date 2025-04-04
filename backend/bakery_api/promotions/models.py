from django.db import models
from django.utils import timezone
from orders.models import Order

# Create your models here.
class Promotion(models.Model):
    promotion_id = models.AutoField(primary_key=True)
    promotion_name = models.CharField(max_length=255)
    discount_rate = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'promotion'

class OrderPromotion(models.Model):
    order_promotion_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)

    class Meta:
        db_table = 'orderpromotion'