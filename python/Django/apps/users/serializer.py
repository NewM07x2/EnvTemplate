from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'views_count', 'likes_count',
            'created_at', 'updated_at'
        ]
