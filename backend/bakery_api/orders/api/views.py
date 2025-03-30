from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from orders.models import Order, OrderDetail
from .serializers import OrderSerializer, OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderSerializer

