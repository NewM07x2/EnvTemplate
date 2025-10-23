"""User repository for data access layer.

Sample repository pattern implementation that can be copied and modified.
This layer handles direct database interactions.
"""

from typing import List, Optional
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

User = get_user_model()


class UserRepository:
    """Repository for User model operations."""
    
    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> QuerySet:
        """Get all users with pagination."""
        return User.objects.all()[skip:skip + limit]
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        """Get user by ID."""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        """Get user by email."""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        """Get user by username."""
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def create(email: str, username: str, password: str, **kwargs) -> User:
        """Create a new user."""
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            **kwargs
        )
        return user
    
    @staticmethod
    def update(user: User, **kwargs) -> User:
        """Update user fields."""
        for field, value in kwargs.items():
            setattr(user, field, value)
        user.save()
        return user
    
    @staticmethod
    def delete(user: User) -> bool:
        """Delete a user."""
        user.delete()
        return True
    
    @staticmethod
    def search(query: str) -> QuerySet:
        """Search users by email, username, or name."""
        return User.objects.filter(
            models.Q(email__icontains=query) |
            models.Q(username__icontains=query) |
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query)
        )
