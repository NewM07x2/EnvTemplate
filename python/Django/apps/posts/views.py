"""Post views (controllers) for REST API.

Sample ViewSet implementation that can be copied and modified.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Post, Category
from .serializers import (
    PostSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    CategorySerializer
)
from .services import PostService, CategoryService


@extend_schema_view(
    list=extend_schema(summary="List all posts", tags=["posts"]),
    retrieve=extend_schema(summary="Get post by ID", tags=["posts"]),
    create=extend_schema(summary="Create new post", tags=["posts"]),
    update=extend_schema(summary="Update post", tags=["posts"]),
    partial_update=extend_schema(summary="Partially update post", tags=["posts"]),
    destroy=extend_schema(summary="Delete post", tags=["posts"]),
)
class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for post operations."""
    
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    service = PostService()
    
    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'create':
            return PostCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PostUpdateSerializer
        return PostSerializer
    
    def list(self, request, *args, **kwargs):
        """List all posts with pagination."""
        skip = int(request.query_params.get('skip', 0))
        limit = int(request.query_params.get('limit', 100))
        published_only = request.query_params.get('published', 'false').lower() == 'true'
        
        posts = self.service.get_posts(skip=skip, limit=limit, published_only=published_only)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        """Retrieve a single post and increment views."""
        post = self.service.get_post(post_id=int(pk))
        
        # Increment views count
        if not request.user.is_authenticated or request.user.id != post.author_id:
            self.service.increment_views(post_id=int(pk))
        
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Create a new post."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        post = self.service.create_post(
            author_id=request.user.id,
            **serializer.validated_data
        )
        output_serializer = PostSerializer(post)
        
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None, *args, **kwargs):
        """Update a post."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        post = self.service.update_post(
            post_id=int(pk),
            user_id=request.user.id,
            is_staff=request.user.is_staff,
            **serializer.validated_data
        )
        output_serializer = PostSerializer(post)
        
        return Response(output_serializer.data)
    
    def destroy(self, request, pk=None, *args, **kwargs):
        """Delete a post."""
        self.service.delete_post(
            post_id=int(pk),
            user_id=request.user.id,
            is_staff=request.user.is_staff
        )
        return Response(
            {'message': 'Post deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @extend_schema(
        summary="Get posts by author",
        tags=["posts"],
    )
    @action(detail=False, methods=['get'])
    def by_author(self, request):
        """Get posts by author ID."""
        author_id = int(request.query_params.get('author_id'))
        skip = int(request.query_params.get('skip', 0))
        limit = int(request.query_params.get('limit', 100))
        
        posts = self.service.get_posts_by_author(
            author_id=author_id,
            skip=skip,
            limit=limit
        )
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Search posts",
        tags=["posts"],
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search posts."""
        query = request.query_params.get('q', '')
        posts = self.service.search_posts(query=query)
        serializer = PostSerializer(posts, many=True)
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
