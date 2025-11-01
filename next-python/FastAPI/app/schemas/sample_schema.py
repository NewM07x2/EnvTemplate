"""Sample Pydantic schemas for request/response validation.

This file contains sample schemas that can be copied and modified
for your own use cases.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ==================== User Schemas ====================

class UserBase(BaseModel):
    """Base user schema with common fields."""
    
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    first_name: Optional[str] = Field(None, max_length=50, description="First name")
    last_name: Optional[str] = Field(None, max_length=50, description="Last name")


class UserCreate(UserBase):
    """Schema for creating a new user."""
    
    password: str = Field(..., min_length=8, description="User password")


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response."""
    
    id: str = Field(..., description="User ID")
    is_active: bool = Field(..., description="Is user active")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = {"from_attributes": True}


# ==================== Post Schemas ====================

class PostBase(BaseModel):
    """Base post schema with common fields."""
    
    title: str = Field(..., min_length=1, max_length=200, description="Post title")
    content: Optional[str] = Field(None, description="Post content")
    published: bool = Field(default=False, description="Is post published")


class PostCreate(PostBase):
    """Schema for creating a new post."""
    
    author_id: str = Field(..., description="Author user ID")


class PostUpdate(BaseModel):
    """Schema for updating a post."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    published: Optional[bool] = None


class PostResponse(PostBase):
    """Schema for post response."""
    
    id: str = Field(..., description="Post ID")
    author_id: str = Field(..., description="Author user ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = {"from_attributes": True}


# ==================== Generic Response Schemas ====================

class MessageResponse(BaseModel):
    """Generic message response schema."""
    
    message: str = Field(..., description="Response message")


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
