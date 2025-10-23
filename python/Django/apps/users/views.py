"""User views (controllers) for REST API.

Sample ViewSet implementation that can be copied and modified.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer
)
from .services import UserService

User = get_user_model()


@extend_schema_view(
    list=extend_schema(summary="List all users", tags=["users"]),
    retrieve=extend_schema(summary="Get user by ID", tags=["users"]),
    create=extend_schema(summary="Create new user", tags=["users"]),
    update=extend_schema(summary="Update user", tags=["users"]),
    partial_update=extend_schema(summary="Partially update user", tags=["users"]),
    destroy=extend_schema(summary="Delete user", tags=["users"]),
)
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for user operations."""
    
    queryset = User.objects.all()
    service = UserService()
    
    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        """Return appropriate permissions."""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def list(self, request, *args, **kwargs):
        """List all users with pagination."""
        skip = int(request.query_params.get('skip', 0))
        limit = int(request.query_params.get('limit', 100))
        
        users = self.service.get_users(skip=skip, limit=limit)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        """Retrieve a single user."""
        user = self.service.get_user(user_id=int(pk))
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Create a new user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = self.service.create_user(**serializer.validated_data)
        output_serializer = UserSerializer(user)
        
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None, *args, **kwargs):
        """Update a user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = self.service.update_user(user_id=int(pk), **serializer.validated_data)
        output_serializer = UserSerializer(user)
        
        return Response(output_serializer.data)
    
    def destroy(self, request, pk=None, *args, **kwargs):
        """Delete a user."""
        self.service.delete_user(user_id=int(pk))
        return Response(
            {'message': 'User deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @extend_schema(
        summary="Change password",
        tags=["users"],
        request=ChangePasswordSerializer,
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request, pk=None):
        """Change user password."""
        user = self.service.get_user(user_id=int(pk))
        
        # Check if user can change this password
        if request.user.id != user.id and not request.user.is_staff:
            return Response(
                {'error': 'You can only change your own password'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.service.change_password(
            user=user,
            old_password=serializer.validated_data['old_password'],
            new_password=serializer.validated_data['new_password']
        )
        
        return Response({'message': 'Password changed successfully'})
    
    @extend_schema(summary="Get current user", tags=["users"])
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current authenticated user."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
