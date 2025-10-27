"""Sample repository for data access layer.

Sample repository pattern implementation that can be copied and modified.
"""

from typing import List, Optional
from django.db.models import QuerySet, Q
from .models import Sample, Category


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


class SampleRepository:
    """Repository for Sample model operations."""
    
    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> QuerySet:
        """Get all samples with pagination."""
        return Sample.objects.select_related('author', 'category').all()[skip:skip + limit]
    
    @staticmethod
    def get_published(skip: int = 0, limit: int = 100) -> QuerySet:
        """Get all published samples with pagination."""
        return Sample.objects.filter(
            is_published=True
        ).select_related('author', 'category').all()[skip:skip + limit]
    
    @staticmethod
    def get_by_id(sample_id: int) -> Optional[Sample]:
        """Get Sample by ID."""
        try:
            return Sample.objects.select_related('author', 'category').get(id=sample_id)
        except Sample.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_slug(slug: str) -> Optional[Sample]:
        """Get Sample by slug."""
        try:
            return Sample.objects.select_related('author', 'category').get(slug=slug)
        except Sample.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_author(author_id: int, skip: int = 0, limit: int = 100) -> QuerySet:
        """Get samples by author."""
        return Sample.objects.filter(
            author_id=author_id
        ).select_related('author', 'category').all()[skip:skip + limit]
    
    @staticmethod
    def get_by_category(category_id: int, skip: int = 0, limit: int = 100) -> QuerySet:
        """Get samples by category."""
        return Sample.objects.filter(
            category_id=category_id
        ).select_related('author', 'category').all()[skip:skip + limit]
    
    @staticmethod
    def create(author_id: int, **kwargs) -> Sample:
        """Create a new sample."""
        sample = Sample.objects.create(author_id=author_id, **kwargs)
        return sample
    
    @staticmethod
    def update(sample: Sample, **kwargs) -> Sample:
        """Update sample fields."""
        for field, value in kwargs.items():
            setattr(sample, field, value)
        sample.save()
        return sample
    
    @staticmethod
    def delete(sample: Sample) -> bool:
        """Delete a sample."""
        sample.delete()
        return True
    
    @staticmethod
    def increment_views(sample: Sample) -> Sample:
        """Increment sample views count."""
        sample.views_count += 1
        sample.save(update_fields=['views_count'])
        return sample
    
    @staticmethod
    def search(query: str) -> QuerySet:
        """Search samples by title or content."""
        return Sample.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        ).select_related('author', 'category')
