from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from customers.models import Customers
from .serializers import CustomersSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer

