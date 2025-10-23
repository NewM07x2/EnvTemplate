"""Post serializers for REST API.

Sample serializers that can be copied and modified.
"""

from rest_framework import serializers
from .models import Post, Category
from apps.users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    """Post serializer for read operations."""
    
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt',
            'author', 'category', 'is_published', 'published_at',
            'views_count', 'likes_count', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'views_count', 'likes_count',
            'created_at', 'updated_at'
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    """Post serializer for create operations."""
    
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'content', 'excerpt',
            'category', 'is_published', 'published_at'
        ]


class PostUpdateSerializer(serializers.ModelSerializer):
    """Post serializer for update operations."""
    
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'content', 'excerpt',
            'category', 'is_published', 'published_at'
        ]
