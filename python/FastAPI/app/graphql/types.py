"""GraphQL schema and types using Strawberry.

This file contains sample GraphQL types and schema that can be copied
and modified for your own use cases.
"""

from datetime import datetime
from typing import Optional

import strawberry


# ==================== GraphQL Types ====================

@strawberry.type
class User:
    """GraphQL User 型

    システム内のユーザーを表し、基本的なプロフィール情報を含みます。
    """

    id: str
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime


@strawberry.type
class Post:
    """GraphQL Post 型

    ユーザーが作成したブログ記事や投稿を表します。
    """

    id: str
    title: str
    content: Optional[str]
    published: bool
    author_id: str
    created_at: datetime
    updated_at: datetime


# ==================== Input Types ====================

@strawberry.input
class UserCreateInput:
    """ユーザー作成用の入力型

    新しいユーザーを作成する際に必要なデータを提供します。
    """

    email: str
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@strawberry.input
class UserUpdateInput:
    """Input type for updating a user."""
    
    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None


@strawberry.input
class PostCreateInput:
    """Input type for creating a post."""
    
    title: str
    content: Optional[str] = None
    published: bool = False
    author_id: str


@strawberry.input
class PostUpdateInput:
    """Input type for updating a post."""
    
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
