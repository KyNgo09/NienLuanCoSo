from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from orders.models import Orders
from .serializers import OrdersSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

