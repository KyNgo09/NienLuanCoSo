from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UnitViewSet, IngredientViewSet

router = DefaultRouter()
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')


urlpatterns = [
    path('', include(router.urls)),  
]