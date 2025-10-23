"""Sample repository for data access layer.

This file contains sample repository patterns that can be copied
and modified for your own use cases.
"""

from typing import List, Optional

from app.core.database import prisma
from app.schemas.sample_schema import PostCreate, PostUpdate, UserCreate, UserUpdate


class UserRepository:
    """Repository for User model."""
    
    @staticmethod
    async def create(user_data: UserCreate, hashed_password: str) -> dict:
        """Create a new user."""
        user = await prisma.user.create(
            data={
                "email": user_data.email,
                "username": user_data.username,
                "password": hashed_password,
                "firstname": user_data.first_name,
                "lastname": user_data.last_name,
            }
        )
        return user.model_dump()
    
    @staticmethod
    async def get_by_id(user_id: str) -> Optional[dict]:
        """Get user by ID."""
        user = await prisma.user.find_unique(where={"id": user_id})
        return user.model_dump() if user else None
    
    @staticmethod
    async def get_by_email(email: str) -> Optional[dict]:
        """Get user by email."""
        user = await prisma.user.find_unique(where={"email": email})
        return user.model_dump() if user else None
    
    @staticmethod
    async def get_by_username(username: str) -> Optional[dict]:
        """Get user by username."""
        user = await prisma.user.find_unique(where={"username": username})
        return user.model_dump() if user else None
    
    @staticmethod
    async def get_all(skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all users with pagination."""
        users = await prisma.user.find_many(skip=skip, take=limit)
        return [user.model_dump() for user in users]
    
    @staticmethod
    async def update(user_id: str, user_data: UserUpdate) -> Optional[dict]:
        """Update a user."""
        update_data = {}
        
        if user_data.email is not None:
            update_data["email"] = user_data.email
        if user_data.username is not None:
            update_data["username"] = user_data.username
        if user_data.first_name is not None:
            update_data["firstname"] = user_data.first_name
        if user_data.last_name is not None:
            update_data["lastname"] = user_data.last_name
        if user_data.is_active is not None:
            update_data["isactive"] = user_data.is_active
        
        if not update_data:
            return None
        
        user = await prisma.user.update(where={"id": user_id}, data=update_data)
        return user.model_dump() if user else None
    
    @staticmethod
    async def delete(user_id: str) -> bool:
        """Delete a user."""
        try:
            await prisma.user.delete(where={"id": user_id})
            return True
        except Exception:
            return False


class PostRepository:
    """Repository for Post model."""
    
    @staticmethod
    async def create(post_data: PostCreate) -> dict:
        """Create a new post."""
        post = await prisma.post.create(
            data={
                "title": post_data.title,
                "content": post_data.content,
                "published": post_data.published,
                "authorid": post_data.author_id,
            }
        )
        return post.model_dump()
    
    @staticmethod
    async def get_by_id(post_id: str) -> Optional[dict]:
        """Get post by ID."""
        post = await prisma.post.find_unique(where={"id": post_id})
        return post.model_dump() if post else None
    
    @staticmethod
    async def get_all(skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all posts with pagination."""
        posts = await prisma.post.find_many(skip=skip, take=limit)
        return [post.model_dump() for post in posts]
    
    @staticmethod
    async def get_by_author(author_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get posts by author with pagination."""
        posts = await prisma.post.find_many(
            where={"authorid": author_id}, skip=skip, take=limit
        )
        return [post.model_dump() for post in posts]
    
    @staticmethod
    async def update(post_id: str, post_data: PostUpdate) -> Optional[dict]:
        """Update a post."""
        update_data = {}
        
        if post_data.title is not None:
            update_data["title"] = post_data.title
        if post_data.content is not None:
            update_data["content"] = post_data.content
        if post_data.published is not None:
            update_data["published"] = post_data.published
        
        if not update_data:
            return None
        
        post = await prisma.post.update(where={"id": post_id}, data=update_data)
        return post.model_dump() if post else None
    
    @staticmethod
    async def delete(post_id: str) -> bool:
        """Delete a post."""
        try:
            await prisma.post.delete(where={"id": post_id})
            return True
        except Exception:
            return False
