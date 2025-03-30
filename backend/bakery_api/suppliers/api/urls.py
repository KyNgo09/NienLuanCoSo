from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, SupplyOrderViewSet, SupplyOrderDetailViewSet

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'supply_orders', SupplyOrderViewSet, basename='supplyorder')
router.register(r'supply_order_details', SupplyOrderDetailViewSet, basename='supplyorderdetail')


urlpatterns = [
    path('', include(router.urls)),  
]