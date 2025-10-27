"""Post models.

Sample model that can be copied and modified for your own use cases.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Category model for posts."""
    
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Sample(models.Model):
    """Sample model.
    
    Sample implementation that can be customized for your needs.
    """
    
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255, unique=True)
    content = models.TextField(_('content'))
    excerpt = models.TextField(_('excerpt'), blank=True, null=True)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('author')
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name=_('category')
    )
    
    is_published = models.BooleanField(_('published'), default=False)
    published_at = models.DateTimeField(_('published at'), null=True, blank=True)
    
    views_count = models.IntegerField(_('views count'), default=0)
    likes_count = models.IntegerField(_('likes count'), default=0)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_published', '-published_at']),
            models.Index(fields=['author', '-created_at']),
        ]
    
    def __str__(self):
        return self.title
