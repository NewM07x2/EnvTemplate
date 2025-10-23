"""Post service layer for business logic.

Sample service layer implementation that can be copied and modified.
"""

from typing import List, Optional
from django.utils import timezone
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from .models import Post, Category
from .repositories import PostRepository, CategoryRepository


class PostService:
    """Service for post-related business logic."""
    
    def __init__(self):
        self.repository = PostRepository()
        self.category_repository = CategoryRepository()
    
    def get_posts(self, skip: int = 0, limit: int = 100, published_only: bool = False) -> List[Post]:
        """Get all posts with pagination."""
        if skip < 0 or limit < 1:
            raise ValidationError('Invalid pagination parameters')
        
        if published_only:
            return list(self.repository.get_published(skip, limit))
        return list(self.repository.get_all(skip, limit))
    
    def get_post(self, post_id: int) -> Post:
        """Get post by ID."""
        post = self.repository.get_by_id(post_id)
        if not post:
            raise NotFound(f'Post with id {post_id} not found')
        return post
    
    def get_post_by_slug(self, slug: str) -> Post:
        """Get post by slug."""
        post = self.repository.get_by_slug(slug)
        if not post:
            raise NotFound(f'Post with slug {slug} not found')
        return post
    
    def get_posts_by_author(self, author_id: int, skip: int = 0, limit: int = 100) -> List[Post]:
        """Get posts by author."""
        return list(self.repository.get_by_author(author_id, skip, limit))
    
    def get_posts_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[Post]:
        """Get posts by category."""
        return list(self.repository.get_by_category(category_id, skip, limit))
    
    def create_post(self, author_id: int, **kwargs) -> Post:
        """Create a new post."""
        # Validate category if provided
        category_id = kwargs.get('category_id')
        if category_id:
            category = self.category_repository.get_by_id(category_id)
            if not category:
                raise ValidationError({'category': f'Category with id {category_id} not found'})
        
        # Set published_at if publishing
        if kwargs.get('is_published') and not kwargs.get('published_at'):
            kwargs['published_at'] = timezone.now()
        
        post = self.repository.create(author_id=author_id, **kwargs)
        return post
    
    def update_post(self, post_id: int, user_id: int, is_staff: bool = False, **kwargs) -> Post:
        """Update post information."""
        post = self.get_post(post_id)
        
        # Check permissions
        if post.author_id != user_id and not is_staff:
            raise PermissionDenied('You can only update your own posts')
        
        # Validate category if being updated
        category_id = kwargs.get('category_id')
        if category_id:
            category = self.category_repository.get_by_id(category_id)
            if not category:
                raise ValidationError({'category': f'Category with id {category_id} not found'})
        
        # Set published_at when publishing for the first time
        if kwargs.get('is_published') and not post.is_published:
            kwargs['published_at'] = timezone.now()
        
        post = self.repository.update(post, **kwargs)
        return post
    
    def delete_post(self, post_id: int, user_id: int, is_staff: bool = False) -> bool:
        """Delete a post."""
        post = self.get_post(post_id)
        
        # Check permissions
        if post.author_id != user_id and not is_staff:
            raise PermissionDenied('You can only delete your own posts')
        
        return self.repository.delete(post)
    
    def increment_views(self, post_id: int) -> Post:
        """Increment post views count."""
        post = self.get_post(post_id)
        return self.repository.increment_views(post)
    
    def search_posts(self, query: str) -> List[Post]:
        """Search posts."""
        return list(self.repository.search(query))


class CategoryService:
    """Service for category-related business logic."""
    
    def __init__(self):
        self.repository = CategoryRepository()
    
    def get_categories(self) -> List[Category]:
        """Get all categories."""
        return list(self.repository.get_all())
    
    def get_category(self, category_id: int) -> Category:
        """Get category by ID."""
        category = self.repository.get_by_id(category_id)
        if not category:
            raise NotFound(f'Category with id {category_id} not found')
        return category
