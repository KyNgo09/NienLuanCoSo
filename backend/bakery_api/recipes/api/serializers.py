from rest_framework import serializers
from recipes.models import Recipe, RecipeDetail

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class RecipeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeDetail
        fields = '__all__'
