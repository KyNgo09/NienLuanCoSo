from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderDetailViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order_details', OrderDetailViewSet, basename='order_detail')


urlpatterns = [
    path('', include(router.urls)),
]