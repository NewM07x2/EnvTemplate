"""Sample REST API endpoints (controllers).

This file contains sample API endpoints that can be copied
and modified for your own use cases.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.sample_schema import (
    MessageResponse,
    PostCreate,
    PostResponse,
    PostUpdate,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.services.sample_service import PostService, UserService

router = APIRouter()


# ==================== User Endpoints ====================

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
    summary="Create a new user",
)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(lambda: UserService()),
) -> UserResponse:
    """Create a new user."""
    return await user_service.create_user(user_data)


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["users"],
    summary="Get user by ID",
)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(lambda: UserService()),
) -> UserResponse:
    """Get a user by ID."""
    return await user_service.get_user(user_id)


@router.get(
    "/users",
    response_model=List[UserResponse],
    tags=["users"],
    summary="Get all users",
)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    user_service: UserService = Depends(lambda: UserService()),
) -> List[UserResponse]:
    """Get all users with pagination."""
    return await user_service.get_users(skip=skip, limit=limit)


@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["users"],
    summary="Update a user",
)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    user_service: UserService = Depends(lambda: UserService()),
) -> UserResponse:
    """Update a user."""
    return await user_service.update_user(user_id, user_data)


@router.delete(
    "/users/{user_id}",
    response_model=MessageResponse,
    tags=["users"],
    summary="Delete a user",
)
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(lambda: UserService()),
) -> MessageResponse:
    """Delete a user."""
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user",
        )
    return MessageResponse(message="User deleted successfully")


# ==================== Post Endpoints ====================

@router.post(
    "/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["posts"],
    summary="Create a new post",
)
async def create_post(
    post_data: PostCreate,
    post_service: PostService = Depends(lambda: PostService()),
) -> PostResponse:
    """Create a new post."""
    return await post_service.create_post(post_data)


@router.get(
    "/posts/{post_id}",
    response_model=PostResponse,
    tags=["posts"],
    summary="Get post by ID",
)
async def get_post(
    post_id: str,
    post_service: PostService = Depends(lambda: PostService()),
) -> PostResponse:
    """Get a post by ID."""
    return await post_service.get_post(post_id)


@router.get(
    "/posts",
    response_model=List[PostResponse],
    tags=["posts"],
    summary="Get all posts",
)
async def get_posts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    post_service: PostService = Depends(lambda: PostService()),
) -> List[PostResponse]:
    """Get all posts with pagination."""
    return await post_service.get_posts(skip=skip, limit=limit)


@router.get(
    "/users/{author_id}/posts",
    response_model=List[PostResponse],
    tags=["posts"],
    summary="Get posts by author",
)
async def get_posts_by_author(
    author_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    post_service: PostService = Depends(lambda: PostService()),
) -> List[PostResponse]:
    """Get all posts by a specific author with pagination."""
    return await post_service.get_posts_by_author(author_id, skip=skip, limit=limit)


@router.put(
    "/posts/{post_id}",
    response_model=PostResponse,
    tags=["posts"],
    summary="Update a post",
)
async def update_post(
    post_id: str,
    post_data: PostUpdate,
    post_service: PostService = Depends(lambda: PostService()),
) -> PostResponse:
    """Update a post."""
    return await post_service.update_post(post_id, post_data)


@router.delete(
    "/posts/{post_id}",
    response_model=MessageResponse,
    tags=["posts"],
    summary="Delete a post",
)
async def delete_post(
    post_id: str,
    post_service: PostService = Depends(lambda: PostService()),
) -> MessageResponse:
    """Delete a post."""
    success = await post_service.delete_post(post_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete post",
        )
    return MessageResponse(message="Post deleted successfully")
