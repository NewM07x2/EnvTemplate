"""Sample service layer for business logic.

This file contains sample service patterns that can be copied
and modified for your own use cases.
"""

from typing import List, Optional

from fastapi import HTTPException, status

from app.core.security import get_password_hash, verify_password
from app.repositories.sample_repository import PostRepository, UserRepository
from app.schemas.sample_schema import (
    PostCreate,
    PostResponse,
    PostUpdate,
    UserCreate,
    UserResponse,
    UserUpdate,
)


class UserService:
    """Service for User business logic."""
    
    def __init__(self) -> None:
        self.repository = UserRepository()
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user."""
        # Check if user already exists
        existing_user = await self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        existing_user = await self.repository.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user
        user = await self.repository.create(user_data, hashed_password)
        return UserResponse(**user)
    
    async def get_user(self, user_id: str) -> UserResponse:
        """Get user by ID."""
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserResponse(**user)
    
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get all users with pagination."""
        users = await self.repository.get_all(skip=skip, limit=limit)
        return [UserResponse(**user) for user in users]
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> UserResponse:
        """Update a user."""
        # Check if user exists
        existing_user = await self.repository.get_by_id(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        # Check email uniqueness if updating email
        if user_data.email:
            email_user = await self.repository.get_by_email(user_data.email)
            if email_user and email_user["id"] != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )
        
        # Check username uniqueness if updating username
        if user_data.username:
            username_user = await self.repository.get_by_username(user_data.username)
            if username_user and username_user["id"] != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken",
                )
        
        # Update user
        user = await self.repository.update(user_id, user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update",
            )
        
        return UserResponse(**user)
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete a user."""
        # Check if user exists
        existing_user = await self.repository.get_by_id(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        return await self.repository.delete(user_id)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[UserResponse]:
        """Authenticate a user."""
        user = await self.repository.get_by_email(email)
        if not user:
            return None
        
        if not verify_password(password, user["password"]):
            return None
        
        return UserResponse(**user)


class PostService:
    """Service for Post business logic."""
    
    def __init__(self) -> None:
        self.repository = PostRepository()
        self.user_repository = UserRepository()
    
    async def create_post(self, post_data: PostCreate) -> PostResponse:
        """Create a new post."""
        # Check if author exists
        author = await self.user_repository.get_by_id(post_data.author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found",
            )
        
        # Create post
        post = await self.repository.create(post_data)
        return PostResponse(**post)
    
    async def get_post(self, post_id: str) -> PostResponse:
        """Get post by ID."""
        post = await self.repository.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )
        return PostResponse(**post)
    
    async def get_posts(self, skip: int = 0, limit: int = 100) -> List[PostResponse]:
        """Get all posts with pagination."""
        posts = await self.repository.get_all(skip=skip, limit=limit)
        return [PostResponse(**post) for post in posts]
    
    async def get_posts_by_author(
        self, author_id: str, skip: int = 0, limit: int = 100
    ) -> List[PostResponse]:
        """Get posts by author with pagination."""
        # Check if author exists
        author = await self.user_repository.get_by_id(author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found",
            )
        
        posts = await self.repository.get_by_author(author_id, skip=skip, limit=limit)
        return [PostResponse(**post) for post in posts]
    
    async def update_post(self, post_id: str, post_data: PostUpdate) -> PostResponse:
        """Update a post."""
        # Check if post exists
        existing_post = await self.repository.get_by_id(post_id)
        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )
        
        # Update post
        post = await self.repository.update(post_id, post_data)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update",
            )
        
        return PostResponse(**post)
    
    async def delete_post(self, post_id: str) -> bool:
        """Delete a post."""
        # Check if post exists
        existing_post = await self.repository.get_by_id(post_id)
        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )
        
        return await self.repository.delete(post_id)
