"""User service layer for business logic.

Sample service layer implementation that can be copied and modified.
This layer contains business logic and validation.
"""

from typing import List, Optional
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, NotFound
from .repositories import UserRepository

User = get_user_model()


class UserService:
    """Service for user-related business logic."""
    
    def __init__(self):
        self.repository = UserRepository()
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        if skip < 0 or limit < 1:
            raise ValidationError('Invalid pagination parameters')
        return list(self.repository.get_all(skip, limit))
    
    def get_user(self, user_id: int) -> User:
        """Get user by ID."""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFound(f'User with id {user_id} not found')
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.repository.get_by_email(email)
    
    def create_user(self, email: str, username: str, password: str, **kwargs) -> User:
        """Create a new user."""
        # Check if email already exists
        if self.repository.get_by_email(email):
            raise ValidationError({'email': 'User with this email already exists'})
        
        # Check if username already exists
        if self.repository.get_by_username(username):
            raise ValidationError({'username': 'User with this username already exists'})
        
        # Create user
        user = self.repository.create(
            email=email,
            username=username,
            password=password,
            **kwargs
        )
        return user
    
    def update_user(self, user_id: int, **kwargs) -> User:
        """Update user information."""
        user = self.get_user(user_id)
        
        # Remove fields that shouldn't be updated directly
        kwargs.pop('password', None)
        kwargs.pop('email', None)  # Require separate email change flow
        
        user = self.repository.update(user, **kwargs)
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        user = self.get_user(user_id)
        return self.repository.delete(user)
    
    def change_password(self, user: User, old_password: str, new_password: str) -> bool:
        """Change user password."""
        if not user.check_password(old_password):
            raise ValidationError({'old_password': 'Incorrect password'})
        
        user.set_password(new_password)
        user.save()
        return True
    
    def verify_user(self, user_id: int) -> User:
        """Verify a user."""
        user = self.get_user(user_id)
        user.is_verified = True
        user.save()
        return user
