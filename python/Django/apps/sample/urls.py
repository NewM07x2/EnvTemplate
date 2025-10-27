"""Post URLs."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'samples', PostViewSet, basename='sample')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
