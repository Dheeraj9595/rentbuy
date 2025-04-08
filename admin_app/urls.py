from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClothViewSet, UserViewSet, RentalViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'cloths', ClothViewSet, basename='cloth')
router.register(r'rental', RentalViewSet, basename='rental')
router.register(r'transaction', TransactionViewSet, basename='transaction')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
