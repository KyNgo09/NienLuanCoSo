from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from promotions.models import Promotion, OrderPromotion
from .serializers import PromotionSerializer, OrderPromotionSerializer

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class OrderPromotionViewSet(viewsets.ModelViewSet):
    queryset = OrderPromotion.objects.all()
    serializer_class = OrderPromotionSerializer
