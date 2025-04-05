from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UnitViewSet, IngredientViewSet, unit_list_create, delete_unit, ingredient_list_create, delete_ingredient

router = DefaultRouter()
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')


urlpatterns = [
    path('', include(router.urls)),  
    path('api/categories/', unit_list_create),
    path('api/categories/<int:unit_id>/', delete_unit, name='delete-unit'),
    path('api/categories/', ingredient_list_create),
    path('api/categories/<int:unit_id>/', delete_ingredient, name='delete-ingredient')
]