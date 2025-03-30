from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PromotionViewSet, OrderPromotionViewSet

router = DefaultRouter()
router.register(r'promotions', PromotionViewSet, basename='promotion')
router.register(r'order_promotions', OrderPromotionViewSet, basename='orderpromotion')

urlpatterns = [
    path('', include(router.urls)),  
]