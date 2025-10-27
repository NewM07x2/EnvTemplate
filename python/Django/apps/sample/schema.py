"""Sample GraphQL schema.

Sample GraphQL types, queries, and mutations that can be copied and modified.
"""

import graphene
from graphene_django import DjangoObjectType
from .models import Sample, Category
from .services import SampleService, CategoryService
from apps.users.schema import UserType


class CategoryType(DjangoObjectType):
    """GraphQL type for Category model."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at']


class SampleType(DjangoObjectType):
    """GraphQL type for Sample model."""
    
    author = graphene.Field(UserType)
    category = graphene.Field(CategoryType)
    
    class Meta:
        model = Sample
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt',
            'author', 'category', 'is_published', 'published_at',
            'views_count', 'likes_count', 'created_at', 'updated_at'
        ]


class SampleInput(graphene.InputObjectType):
    """Input type for creating samples."""
    title = graphene.String(required=True)
    slug = graphene.String(required=True)
    content = graphene.String(required=True)
    excerpt = graphene.String()
    category_id = graphene.Int()
    is_published = graphene.Boolean(default_value=False)


class SampleUpdateInput(graphene.InputObjectType):
    """Input type for updating samples."""
    title = graphene.String()
    slug = graphene.String()
    content = graphene.String()
    excerpt = graphene.String()
    category_id = graphene.Int()
    is_published = graphene.Boolean()


class SampleQuery(graphene.ObjectType):
    """Sample queries."""
    
    samples = graphene.List(
        SampleType,
        skip=graphene.Int(default_value=0),
        limit=graphene.Int(default_value=100),
        published_only=graphene.Boolean(default_value=False)
    )
    sample = graphene.Field(SampleType, id=graphene.Int(required=True))
    sample_by_slug = graphene.Field(SampleType, slug=graphene.String(required=True))
    samples_by_author = graphene.List(
        SampleType,
        author_id=graphene.Int(required=True),
        skip=graphene.Int(default_value=0),
        limit=graphene.Int(default_value=100)
    )
    categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.Int(required=True))
    
    def resolve_samples(self, info, skip=0, limit=100, published_only=False):
        """Get all samples with pagination."""
        service = SampleService()
        return service.get_samples(skip=skip, limit=limit, published_only=published_only)
    
    def resolve_sample(self, info, id):
        """Get sample by ID."""
        service = SampleService()
        return service.get_sample(sample_id=id)
    
    def resolve_sample_by_slug(self, info, slug):
        """Get sample by slug."""
        service = SampleService()
        return service.get_sample_by_slug(slug=slug)
    
    def resolve_samples_by_author(self, info, author_id, skip=0, limit=100):
        """Get samples by author."""
        service = SampleService()
        return service.get_samples_by_author(author_id=author_id, skip=skip, limit=limit)
    
    def resolve_categories(self, info):
        """Get all categories."""
        service = CategoryService()
        return service.get_categories()
    
    def resolve_category(self, info, id):
        """Get category by ID."""
        service = CategoryService()
        return service.get_category(category_id=id)


class CreateSample(graphene.Mutation):
    """Mutation to create a new sample."""
    
    class Arguments:
        input = SampleInput(required=True)
        author_id = graphene.Int(required=True)
    
    sample = graphene.Field(SampleType)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, input, author_id):
        """Create new sample."""
        service = SampleService()
        try:
            sample = service.create_sample(
                author_id=author_id,
                **input.__dict__
            )
            return CreateSample(sample=sample, success=True, message='Sample created successfully')
        except Exception as e:
            return CreateSample(sample=None, success=False, message=str(e))


class UpdateSample(graphene.Mutation):
    """Mutation to update a sample."""
    
    class Arguments:
        id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)
        input = SampleUpdateInput(required=True)
        is_staff = graphene.Boolean(default_value=False)
    
    sample = graphene.Field(sampleType)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, id, user_id, input, is_staff=False):
        """Update sample."""
        service = SampleService()
        try:
            sample = service.update_sample(
                sample_id=id,
                user_id=user_id,
                is_staff=is_staff,
                **input.__dict__
            )
            return UpdateSample(sample=sample, success=True, message='Sample updated successfully')
        except Exception as e:
            return UpdateSample(sample=None, success=False, message=str(e))


class DeleteSample(graphene.Mutation):
    """Mutation to delete a sample."""
    
    class Arguments:
        id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)
        is_staff = graphene.Boolean(default_value=False)
    
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, id, user_id, is_staff=False):
        """Delete sample."""
        service = SampleService()
        try:
            service.delete_sample(sample_id=id, user_id=user_id, is_staff=is_staff)
            return DeleteSample(success=True, message='Sample deleted successfully')
        except Exception as e:
            return DeleteSample(success=False, message=str(e))


class SampleMutation(graphene.ObjectType):
    """Sample mutations."""
    
    create_sample = CreateSample.Field()
    update_sample = UpdateSample.Field()
    delete_sample = DeleteSample.Field()
