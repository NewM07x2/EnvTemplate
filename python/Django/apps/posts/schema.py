"""Post GraphQL schema.

Sample GraphQL types, queries, and mutations that can be copied and modified.
"""

import graphene
from graphene_django import DjangoObjectType
from .models import Post, Category
from .services import PostService, CategoryService
from apps.users.schema import UserType


class CategoryType(DjangoObjectType):
    """GraphQL type for Category model."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at']


class PostType(DjangoObjectType):
    """GraphQL type for Post model."""
    
    author = graphene.Field(UserType)
    category = graphene.Field(CategoryType)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt',
            'author', 'category', 'is_published', 'published_at',
            'views_count', 'likes_count', 'created_at', 'updated_at'
        ]


class PostInput(graphene.InputObjectType):
    """Input type for creating posts."""
    title = graphene.String(required=True)
    slug = graphene.String(required=True)
    content = graphene.String(required=True)
    excerpt = graphene.String()
    category_id = graphene.Int()
    is_published = graphene.Boolean(default_value=False)


class PostUpdateInput(graphene.InputObjectType):
    """Input type for updating posts."""
    title = graphene.String()
    slug = graphene.String()
    content = graphene.String()
    excerpt = graphene.String()
    category_id = graphene.Int()
    is_published = graphene.Boolean()


class PostQuery(graphene.ObjectType):
    """Post queries."""
    
    posts = graphene.List(
        PostType,
        skip=graphene.Int(default_value=0),
        limit=graphene.Int(default_value=100),
        published_only=graphene.Boolean(default_value=False)
    )
    post = graphene.Field(PostType, id=graphene.Int(required=True))
    post_by_slug = graphene.Field(PostType, slug=graphene.String(required=True))
    posts_by_author = graphene.List(
        PostType,
        author_id=graphene.Int(required=True),
        skip=graphene.Int(default_value=0),
        limit=graphene.Int(default_value=100)
    )
    categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.Int(required=True))
    
    def resolve_posts(self, info, skip=0, limit=100, published_only=False):
        """Get all posts with pagination."""
        service = PostService()
        return service.get_posts(skip=skip, limit=limit, published_only=published_only)
    
    def resolve_post(self, info, id):
        """Get post by ID."""
        service = PostService()
        return service.get_post(post_id=id)
    
    def resolve_post_by_slug(self, info, slug):
        """Get post by slug."""
        service = PostService()
        return service.get_post_by_slug(slug=slug)
    
    def resolve_posts_by_author(self, info, author_id, skip=0, limit=100):
        """Get posts by author."""
        service = PostService()
        return service.get_posts_by_author(author_id=author_id, skip=skip, limit=limit)
    
    def resolve_categories(self, info):
        """Get all categories."""
        service = CategoryService()
        return service.get_categories()
    
    def resolve_category(self, info, id):
        """Get category by ID."""
        service = CategoryService()
        return service.get_category(category_id=id)


class CreatePost(graphene.Mutation):
    """Mutation to create a new post."""
    
    class Arguments:
        input = PostInput(required=True)
        author_id = graphene.Int(required=True)
    
    post = graphene.Field(PostType)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, input, author_id):
        """Create new post."""
        service = PostService()
        try:
            post = service.create_post(
                author_id=author_id,
                **input.__dict__
            )
            return CreatePost(post=post, success=True, message='Post created successfully')
        except Exception as e:
            return CreatePost(post=None, success=False, message=str(e))


class UpdatePost(graphene.Mutation):
    """Mutation to update a post."""
    
    class Arguments:
        id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)
        input = PostUpdateInput(required=True)
        is_staff = graphene.Boolean(default_value=False)
    
    post = graphene.Field(PostType)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, id, user_id, input, is_staff=False):
        """Update post."""
        service = PostService()
        try:
            post = service.update_post(
                post_id=id,
                user_id=user_id,
                is_staff=is_staff,
                **input.__dict__
            )
            return UpdatePost(post=post, success=True, message='Post updated successfully')
        except Exception as e:
            return UpdatePost(post=None, success=False, message=str(e))


class DeletePost(graphene.Mutation):
    """Mutation to delete a post."""
    
    class Arguments:
        id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)
        is_staff = graphene.Boolean(default_value=False)
    
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, id, user_id, is_staff=False):
        """Delete post."""
        service = PostService()
        try:
            service.delete_post(post_id=id, user_id=user_id, is_staff=is_staff)
            return DeletePost(success=True, message='Post deleted successfully')
        except Exception as e:
            return DeletePost(success=False, message=str(e))


class PostMutation(graphene.ObjectType):
    """Post mutations."""
    
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
