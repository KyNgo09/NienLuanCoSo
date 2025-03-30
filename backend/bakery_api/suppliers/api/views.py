from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from suppliers.models import Supplier
from .serializers import SupplierSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


