from rest_framework import serializers

from admin_app.models import Cloth, Rental, Transaction, User


class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloth
        fields = "__all__"  # Includes all fields from the model


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "role",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
            "last_login",
        ]
