from rest_framework import serializers
from orders.models import Order, OrderDetail

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'customer': {'required': False}
        }
        
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'
        