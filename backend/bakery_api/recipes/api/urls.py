from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, RecipeDetailViewSet

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)          # URL cho Recipe
router.register(r'recipe_details', RecipeDetailViewSet)  # URL cho RecipeDetail

urlpatterns = [
    path('', include(router.urls)),
]
