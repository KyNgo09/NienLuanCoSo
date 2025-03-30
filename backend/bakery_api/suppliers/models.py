from django.db import models
# from ingredients.models import Ingredient

# Create your models here.
class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    class Meta:
        db_table = 'supplier'

class SupplyOrder(models.Model):
    supply_order_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)  
    order_date = models.DateTimeField(auto_now_add=True) 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  
    class Meta:
        db_table = 'supplyorder'

class SupplyOrderDetail(models.Model):
    supply_order_detail_id = models.AutoField(primary_key=True)
    supply_order = models.ForeignKey(SupplyOrder, on_delete=models.CASCADE) 
    ingredient = models.ForeignKey('ingredients.Ingredient', on_delete=models.CASCADE)  # Dùng chuỗi tham chiếu
    quantity = models.IntegerField()  # Phải xuống dòng để tránh lỗi cú pháp
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)  

    class Meta:
        db_table = 'supplyorderdetail'