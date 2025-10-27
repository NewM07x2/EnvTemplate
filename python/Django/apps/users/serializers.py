from rest_framework import serializers
from .models.user_model import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'date_joined']

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """ユーザーの読み取り操作用シリアライザー。"""
    
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'full_name', 'bio', 'avatar', 'is_verified',
            'is_active', 'is_staff', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """ユーザー作成操作用シリアライザー."""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'password_confirm',
            'first_name', 'last_name', 'bio', 'avatar'
        ]
    
    def validate(self, attrs):
        """パスワードが一致することを確認します."""
        if attrs.get('password') != attrs.pop('password_confirm', None):
            raise serializers.ValidationError({'password': 'パスワードが一致しません'})
        return attrs
    
    def create(self, validated_data):
        """ハッシュ化されたパスワードでユーザーを作成します."""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """ユーザー更新操作用シリアライザー."""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'avatar']


class ChangePasswordSerializer(serializers.Serializer):
    """パスワード変更用シリアライザー."""
    
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    def validate(self, attrs):
        """新しいパスワードが一致することを確認します."""
        if attrs.get('new_password') != attrs.get('new_password_confirm'):
            raise serializers.ValidationError({'new_password': 'パスワードが一致しません'})
        return attrs
