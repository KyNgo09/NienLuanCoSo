from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, category_list_create, delete_category

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')


urlpatterns = [
    path('', include(router.urls)),  
    path('api/categories/', category_list_create),
    path('api/categories/<int:category_id>/', delete_category, name='delete-category')
]