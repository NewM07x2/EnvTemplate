"""Sample serializers for REST API.

Sample serializers that can be copied and modified.
"""

from rest_framework import serializers
from .models import Sample, Category
from apps.users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SampleSerializer(serializers.ModelSerializer):
    """Sample serializer for read operations."""
    
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Sample
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt',
            'author', 'category', 'is_published', 'published_at',
            'views_count', 'likes_count', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'views_count', 'likes_count',
            'created_at', 'updated_at'
        ]


class SampleCreateSerializer(serializers.ModelSerializer):
    """Sample serializer for create operations."""
    
    class Meta:
        model = Sample
        fields = [
            'title', 'slug', 'content', 'excerpt',
            'category', 'is_published', 'published_at'
        ]


class SampleUpdateSerializer(serializers.ModelSerializer):
    """Sample serializer for update operations."""
    
    class Meta:
        model = Sample
        fields = [
            'title', 'slug', 'content', 'excerpt',
            'category', 'is_published', 'published_at'
        ]
