from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from promotions.models import Promotion
from .serializers import PromotionSerializer

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

