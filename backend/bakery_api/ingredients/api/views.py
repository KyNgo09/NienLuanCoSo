from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from ingredients.models import Unit, Ingredient
from .serializers import UnitSerializer, IngredientSerializer

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer