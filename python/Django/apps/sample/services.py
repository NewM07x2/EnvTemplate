"""Sample service layer for business logic.

Sample service layer implementation that can be copied and modified.
"""

from typing import List, Optional
from django.utils import timezone
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from .models import Sample, Category
from .repositories import SampleRepository, CategoryRepository


class SampleService:
    """Service for sample-related business logic."""
    
    def __init__(self):
        self.repository = SampleRepository()
        self.category_repository = CategoryRepository()
    
    def get_samples(self, skip: int = 0, limit: int = 100, published_only: bool = False) -> List[Sample]:
        """Get all samples with pagination."""
        if skip < 0 or limit < 1:
            raise ValidationError('Invalid pagination parameters')
        
        if published_only:
            return list(self.repository.get_published(skip, limit))
        return list(self.repository.get_all(skip, limit))
    
    def get_sample(self, sample_id: int) -> Sample:
        """Get sample by ID."""
        sample = self.repository.get_by_id(sample_id)
        if not sample:
            raise NotFound(f'Sample with id {sample_id} not found')
        return sample
    
    def get_sample_by_slug(self, slug: str) -> Sample:
        """Get sample by slug."""
        sample = self.repository.get_by_slug(slug)
        if not sample:
            raise NotFound(f'Sample with slug {slug} not found')
        return sample
    
    def get_samples_by_author(self, author_id: int, skip: int = 0, limit: int = 100) -> List[Sample]:
        """Get samples by author."""
        return list(self.repository.get_by_author(author_id, skip, limit))
    
    def get_samples_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[Sample]:
        """Get samples by category."""
        return list(self.repository.get_by_category(category_id, skip, limit))
    
    def create_sample(self, author_id: int, **kwargs) -> Sample:
        """Create a new sample."""
        # Validate category if provided
        category_id = kwargs.get('category_id')
        if category_id:
            category = self.category_repository.get_by_id(category_id)
            if not category:
                raise ValidationError({'category': f'Category with id {category_id} not found'})
        
        # Set published_at if publishing
        if kwargs.get('is_published') and not kwargs.get('published_at'):
            kwargs['published_at'] = timezone.now()
        
        sample = self.repository.create(author_id=author_id, **kwargs)
        return sample
    
    def update_sample(self, sample_id: int, user_id: int, is_staff: bool = False, **kwargs) -> Sample:
        """Update sample information."""
        sample = self.get_sample(sample_id)
        
        # Check permissions
        if sample.author_id != user_id and not is_staff:
            raise PermissionDenied('You can only update your own samples')
        
        # Validate category if being updated
        category_id = kwargs.get('category_id')
        if category_id:
            category = self.category_repository.get_by_id(category_id)
            if not category:
                raise ValidationError({'category': f'Category with id {category_id} not found'})
        
        # Set published_at when publishing for the first time
        if kwargs.get('is_published') and not sample.is_published:
            kwargs['published_at'] = timezone.now()
        
        sample = self.repository.update(sample, **kwargs)
        return sample
    
    def delete_sample(self, sample_id: int, user_id: int, is_staff: bool = False) -> bool:
        """Delete a sample."""
        sample = self.get_sample(sample_id)
        
        # Check permissions
        if sample.author_id != user_id and not is_staff:
            raise PermissionDenied('You can only delete your own samples')
        
        return self.repository.delete(sample)
    
    def increment_views(self, sample_id: int) -> Sample:
        """Increment sample views count."""
        sample = self.get_sample(sample_id)
        return self.repository.increment_views(sample)
    
    def search_samples(self, query: str) -> List[Sample]:
        """Search samples."""
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
