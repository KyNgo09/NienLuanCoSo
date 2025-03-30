from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from delivery.models import Delivery
from .serializers import Deliveryerializer

class DelieveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = Deliveryerializer

