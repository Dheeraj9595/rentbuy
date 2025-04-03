from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClothViewSet, UserViewSet

router = DefaultRouter()
router.register(r'cloths', ClothViewSet, basename='cloth')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
