from rest_framework import serializers
from orders.models import Order, OrderDetail
from products.api.serializers import ProductSerializer
from customers.api.serializers import CustomerSerializer

class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Serialize toàn bộ product object

    class Meta:
        model = OrderDetail
        fields = ['order_detail_id', 'order', 'product', 'quantity', 'unit_price', 'sub_total']
        extra_kwargs = {
            'order': {'write_only': True},  
        }

class OrderSerializer(serializers.ModelSerializer):
    items = OrderDetailSerializer(many=True, write_only=True)
    customer = CustomerSerializer(read_only=True)  
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'customer': {'required': False},
            'is_processed': {'required': False}
        }

    def get_is_registered(self, obj):
        return obj.customer.user_id is not None if obj.customer else False