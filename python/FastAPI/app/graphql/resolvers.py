"""Sample GraphQL resolvers.

This file contains sample resolvers that can be copied and modified
for your own use cases.
"""

from typing import List, Optional

import strawberry
from strawberry.types import Info

from app.core.database import prisma
from app.graphql.types import (
    Post,
    PostCreateInput,
    PostUpdateInput,
    User,
    UserCreateInput,
    UserUpdateInput,
)


# ==================== Query Resolvers ====================

@strawberry.type
class Query:
    """GraphQL Query root."""
    
    @strawberry.field
    async def hello(self) -> str:
        """Sample hello query."""
        return "Hello from GraphQL!"
    
    @strawberry.field
    async def users(self, info: Info) -> List[User]:
        """Get all users."""
        users = await prisma.user.find_many()
        return [
            User(
                id=user.id,
                email=user.email,
                username=user.username,
                first_name=user.firstname,
                last_name=user.lastname,
                is_active=user.isactive,
                created_at=user.createdat,
                updated_at=user.updatedat,
            )
            for user in users
        ]
    
    @strawberry.field
    async def user(self, info: Info, id: str) -> Optional[User]:
        """Get user by ID."""
        user = await prisma.user.find_unique(where={"id": id})
        if not user:
            return None
        
        return User(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.firstname,
            last_name=user.lastname,
            is_active=user.isactive,
            created_at=user.createdat,
            updated_at=user.updatedat,
        )
    
    @strawberry.field
    async def posts(self, info: Info) -> List[Post]:
        """Get all posts."""
        posts = await prisma.post.find_many()
        return [
            Post(
                id=post.id,
                title=post.title,
                content=post.content,
                published=post.published,
                author_id=post.authorid,
                created_at=post.createdat,
                updated_at=post.updatedat,
            )
            for post in posts
        ]
    
    @strawberry.field
    async def post(self, info: Info, id: str) -> Optional[Post]:
        """Get post by ID."""
        post = await prisma.post.find_unique(where={"id": id})
        if not post:
            return None
        
        return Post(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            author_id=post.authorid,
            created_at=post.createdat,
            updated_at=post.updatedat,
        )


# ==================== Mutation Resolvers ====================

@strawberry.type
class Mutation:
    """GraphQL Mutation root."""
    
    @strawberry.mutation
    async def create_user(self, info: Info, input: UserCreateInput) -> User:
        """Create a new user."""
        from app.core.security import get_password_hash
        
        user = await prisma.user.create(
            data={
                "email": input.email,
                "username": input.username,
                "password": get_password_hash(input.password),
                "firstname": input.first_name,
                "lastname": input.last_name,
            }
        )
        
        return User(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.firstname,
            last_name=user.lastname,
            is_active=user.isactive,
            created_at=user.createdat,
            updated_at=user.updatedat,
        )
    
    @strawberry.mutation
    async def update_user(
        self, info: Info, id: str, input: UserUpdateInput
    ) -> Optional[User]:
        """Update a user."""
        update_data = {}
        
        if input.email is not None:
            update_data["email"] = input.email
        if input.username is not None:
            update_data["username"] = input.username
        if input.first_name is not None:
            update_data["firstname"] = input.first_name
        if input.last_name is not None:
            update_data["lastname"] = input.last_name
        if input.is_active is not None:
            update_data["isactive"] = input.is_active
        
        if not update_data:
            return None
        
        user = await prisma.user.update(where={"id": id}, data=update_data)
        
        return User(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.firstname,
            last_name=user.lastname,
            is_active=user.isactive,
            created_at=user.createdat,
            updated_at=user.updatedat,
        )
    
    @strawberry.mutation
    async def delete_user(self, info: Info, id: str) -> bool:
        """Delete a user."""
        try:
            await prisma.user.delete(where={"id": id})
            return True
        except Exception:
            return False
    
    @strawberry.mutation
    async def create_post(self, info: Info, input: PostCreateInput) -> Post:
        """Create a new post."""
        post = await prisma.post.create(
            data={
                "title": input.title,
                "content": input.content,
                "published": input.published,
                "authorid": input.author_id,
            }
        )
        
        return Post(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            author_id=post.authorid,
            created_at=post.createdat,
            updated_at=post.updatedat,
        )
    
    @strawberry.mutation
    async def update_post(
        self, info: Info, id: str, input: PostUpdateInput
    ) -> Optional[Post]:
        """Update a post."""
        update_data = {}
        
        if input.title is not None:
            update_data["title"] = input.title
        if input.content is not None:
            update_data["content"] = input.content
        if input.published is not None:
            update_data["published"] = input.published
        
        if not update_data:
            return None
        
        post = await prisma.post.update(where={"id": id}, data=update_data)
        
        return Post(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            author_id=post.authorid,
            created_at=post.createdat,
            updated_at=post.updatedat,
        )
    
    @strawberry.mutation
    async def delete_post(self, info: Info, id: str) -> bool:
        """Delete a post."""
        try:
            await prisma.post.delete(where={"id": id})
            return True
        except Exception:
            return False
