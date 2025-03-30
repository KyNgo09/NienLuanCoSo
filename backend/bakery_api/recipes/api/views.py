from rest_framework import viewsets
from recipes.models import Recipe, RecipeDetail
from .serializers import RecipeSerializer, RecipeDetailSerializer
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class RecipeDetailViewSet(viewsets.ModelViewSet):
    queryset = RecipeDetail.objects.all()
    serializer_class = RecipeDetailSerializer
