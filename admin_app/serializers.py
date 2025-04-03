from rest_framework import serializers
from admin_app.models import Cloth, User


class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloth
        fields = '__all__'  # Includes all fields from the model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'role','username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'last_login']