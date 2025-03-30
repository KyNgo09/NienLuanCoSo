from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from suppliers.models import Supplier, SupplyOrder, SupplyOrderDetail
from .serializers import SupplierSerializer, SupplyOrderDetailSerializer, SupplyOrderSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class SupplyOrderViewSet(viewsets.ModelViewSet):
    queryset = SupplyOrder.objects.all()
    serializer_class = SupplyOrderSerializer

class SupplyOrderDetailViewSet(viewsets.ModelViewSet):
    queryset = SupplyOrderDetail.objects.all()
    serializer_class = SupplyOrderDetailSerializer

