from rest_framework import serializers
from promotions.models import Promotion, OrderPromotion

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'

class OrderPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPromotion
        fields = '__all__'