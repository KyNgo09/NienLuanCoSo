from django.db import models
from accounts.models import User
# Create your models here.
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    loyalty_point = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'customers'
