"""Post repository for data access layer.

Sample repository pattern implementation that can be copied and modified.
"""

from typing import List, Optional
from django.db.models import QuerySet, Q
from .models import Post, Category


class CategoryRepository:
    """Repository for Category model operations."""
    
    @staticmethod
    def get_all() -> QuerySet:
        """Get all categories."""
        return Category.objects.all()
    
    @staticmethod
    def get_by_id(category_id: int) -> Optional[Category]:
        """Get category by ID."""
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_slug(slug: str) -> Optional[Category]:
        """Get category by slug."""
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return None


class PostRepository:
    """Repository for Post model operations."""
    
    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> QuerySet:
        """Get all posts with pagination."""
        return Post.objects.select_related('author', 'category').all()[skip:skip + limit]
    
    @staticmethod
    def get_published(skip: int = 0, limit: int = 100) -> QuerySet:
        """Get all published posts with pagination."""
        return Post.objects.filter(
            is_published=True
        ).select_related('author', 'category').all()[skip:skip + limit]
    
    @staticmethod
    def get_by_id(post_id: int) -> Optional[Post]:
        """Get post by ID."""
        try:
            return Post.objects.select_related('author', 'category').get(id=post_id)
        except Post.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_slug(slug: str) -> Optional[Post]:
        """Get post by slug."""
        try:
            return Post.objects.select_related('author', 'category').get(slug=slug)
        except Post.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_author(author_id: int, skip: int = 0, limit: int = 100) -> QuerySet:
        """Get posts by author."""
        return Post.objects.filter(
            author_id=author_id
        ).select_related('author', 'category').all()[skip:skip + limit]
    
    @staticmethod
    def get_by_category(category_id: int, skip: int = 0, limit: int = 100) -> QuerySet:
        """Get posts by category."""
        return Post.objects.filter(
            category_id=category_id
        ).select_related('author', 'category').all()[skip:skip + limit]
    
    @staticmethod
    def create(author_id: int, **kwargs) -> Post:
        """Create a new post."""
        post = Post.objects.create(author_id=author_id, **kwargs)
        return post
    
    @staticmethod
    def update(post: Post, **kwargs) -> Post:
        """Update post fields."""
        for field, value in kwargs.items():
            setattr(post, field, value)
        post.save()
        return post
    
    @staticmethod
    def delete(post: Post) -> bool:
        """Delete a post."""
        post.delete()
        return True
    
    @staticmethod
    def increment_views(post: Post) -> Post:
        """Increment post views count."""
        post.views_count += 1
        post.save(update_fields=['views_count'])
        return post
    
    @staticmethod
    def search(query: str) -> QuerySet:
        """Search posts by title or content."""
        return Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        ).select_related('author', 'category')
