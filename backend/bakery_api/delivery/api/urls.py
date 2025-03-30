from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DelieveryViewSet

router = DefaultRouter()
router.register(r'delivery', DelieveryViewSet, basename='delivery')

urlpatterns = [
    path('', include(router.urls)),  
]