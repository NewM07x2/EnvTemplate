"""
    Sample views (controllers) for REST API.
    Sample ViewSet implementation that can be copied and modified.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Sample, Category
from .serializers import (
    SampleSerializer,
    SampleCreateSerializer,
    SampleUpdateSerializer,
    CategorySerializer
)
from .services import SampleService, CategoryService


@extend_schema_view(
    list=extend_schema(summary="List all samples", tags=["samples"]),
    retrieve=extend_schema(summary="Get sample by ID", tags=["samples"]),
    create=extend_schema(summary="Create new sample", tags=["samples"]),
    update=extend_schema(summary="Update sample", tags=["samples"]),
    partial_update=extend_schema(summary="Partially update sample", tags=["samples"]),
    destroy=extend_schema(summary="Delete sample", tags=["samples"]),
)
class SampleViewSet(viewsets.ModelViewSet):
    """ViewSet for sample operations."""
    
    queryset = Sample.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    service = SampleService()
    
    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'create':
            return SampleCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SampleUpdateSerializer
        return SampleSerializer
    
    def list(self, request, *args, **kwargs):
        """List all samples with pagination."""
        skip = int(request.query_params.get('skip', 0))
        limit = int(request.query_params.get('limit', 100))
        published_only = request.query_params.get('published', 'false').lower() == 'true'
        
        samples = self.service.get_samples(skip=skip, limit=limit, published_only=published_only)
        serializer = self.get_serializer(samples, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        """Retrieve a single sample and increment views."""
        sample = self.service.get_sample(sample_id=int(pk))
        
        # Increment views count
        if not request.user.is_authenticated or request.user.id != sample.author_id:
            self.service.increment_views(sample_id=int(pk))
        
        serializer = self.get_serializer(sample)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Create a new sample."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        sample = self.service.create_sample(
            author_id=request.user.id,
            **serializer.validated_data
        )
        output_serializer = SampleSerializer(sample)
        
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None, *args, **kwargs):
        """Update a sample."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        sample = self.service.update_sample(
            sample_id=int(pk),
            user_id=request.user.id,
            is_staff=request.user.is_staff,
            **serializer.validated_data
        )
        output_serializer = SampleSerializer(sample)
        
        return Response(output_serializer.data)
    
    def destroy(self, request, pk=None, *args, **kwargs):
        """Delete a sample."""
        self.service.delete_sample(
            sample_id=int(pk),
            user_id=request.user.id,
            is_staff=request.user.is_staff
        )
        return Response(
            {'message': 'Sample deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @extend_schema(
        summary="Get samples by author",
        tags=["samples"],
    )
    @action(detail=False, methods=['get'])
    def by_author(self, request):
        """Get samples by author ID."""
        author_id = int(request.query_params.get('author_id'))
        skip = int(request.query_params.get('skip', 0))
        limit = int(request.query_params.get('limit', 100))
        
        samples = self.service.get_samples_by_author(
            author_id=author_id,
            skip=skip,
            limit=limit
        )
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Search samples",
        tags=["samples"],
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search samples."""
        query = request.query_params.get('q', '')
        samples = self.service.search_samples(query=query)
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="List all categories", tags=["categories"]),
    retrieve=extend_schema(summary="Get category by ID", tags=["categories"]),
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for category operations (read-only)."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    service = CategoryService()
    
    def list(self, request, *args, **kwargs):
        """List all categories."""
        categories = self.service.get_categories()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        """Retrieve a single category."""
        category = self.service.get_category(category_id=int(pk))
        serializer = self.get_serializer(category)
        return Response(serializer.data)
