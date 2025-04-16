from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderDetailViewSet, create_order

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order_details', OrderDetailViewSet, basename='orderdetail')


urlpatterns = [
    path('', include(router.urls)),  
    path('api/orders/', create_order, name='create_order'),
]