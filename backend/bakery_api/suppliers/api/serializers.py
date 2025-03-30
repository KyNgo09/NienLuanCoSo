from rest_framework import serializers
from suppliers.models import Supplier, SupplyOrder, SupplyOrderDetail

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class SupplyOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyOrder
        fields = '__all__'

class SupplyOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyOrderDetail
        fields = '__all__'