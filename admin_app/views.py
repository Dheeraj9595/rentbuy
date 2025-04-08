from http.client import responses

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from admin_app.models import User
from admin_app.serializers import (
    ClothSerializer,
    RentalSerializer,
    TransactionSerializer,
    UserSerializer,
)

from .models import Cloth, Rental, Transaction


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer


class ClothViewSet(viewsets.ModelViewSet):
    queryset = Cloth.objects.all().order_by("-id")
    serializer_class = ClothSerializer
    permission_classes = [IsAdminUser]

    # Approve a cloth listing
    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        cloth = self.get_object()
        cloth.is_approved = True
        cloth.save()
        return Response({"message": f"Cloth '{cloth.name}' approved by admin"})

    # Reject a cloth listing
    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        cloth = self.get_object()
        cloth.is_approved = False
        cloth.save()
        return Response({"message": f"Cloth '{cloth.name}' rejected by admin"})

    @action(detail=True, methods=["post"])
    def hold(self, request, pk=None):
        cloth = self.get_object()
        cloth.is_approved = False
        cloth.save()
        return Response({"message": f"Cloth '{cloth.name}' put on hold by admin"})


class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all().order_by("-id")
    serializer_class = RentalSerializer
    permission_classes = [IsAdminUser]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by("-id")
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]
