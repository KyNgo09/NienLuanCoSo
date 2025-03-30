from rest_framework import serializers
from delivery.models import Delivery

class Deliveryerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'