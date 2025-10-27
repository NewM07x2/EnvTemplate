import graphene
from graphene_django import DjangoObjectType
from ..models import Sample
from ..service.services import SampleService
from apps.users.schema import UserType
from .category_schema import CategoryType

class SampleType(DjangoObjectType):
    """サンプルモデルのGraphQLタイプ。"""
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
    """サンプル作成用の入力タイプ。"""
    title = graphene.String(required=True)
    slug = graphene.String(required=True)
    content = graphene.String(required=True)
    excerpt = graphene.String()
    category_id = graphene.Int()
    is_published = graphene.Boolean(default_value=False)

class SampleUpdateInput(graphene.InputObjectType):
    """サンプル更新用の入力タイプ。"""
    title = graphene.String()
    slug = graphene.String()
    content = graphene.String()
    excerpt = graphene.String()
    category_id = graphene.Int()
    is_published = graphene.Boolean()

class SampleQuery(graphene.ObjectType):
    """サンプルに関するクエリ。"""
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

    def resolve_samples(self, info, skip=0, limit=100, published_only=False):
        """ページネーション付きで全てのサンプルを取得。"""
        service = SampleService()
        return service.get_samples(skip=skip, limit=limit, published_only=published_only)

    def resolve_sample(self, info, id):
        """IDでサンプルを取得。"""
        service = SampleService()
        return service.get_sample(sample_id=id)

    def resolve_sample_by_slug(self, info, slug):
        """スラッグでサンプルを取得。"""
        service = SampleService()
        return service.get_sample_by_slug(slug=slug)

    def resolve_samples_by_author(self, info, author_id, skip=0, limit=100):
        """著者IDでサンプルを取得。"""
        service = SampleService()
        return service.get_samples_by_author(author_id=author_id, skip=skip, limit=limit)

class CreateSample(graphene.Mutation):
    """新しいサンプルを作成するミューテーション。"""
    class Arguments:
        input = SampleInput(required=True)
        author_id = graphene.Int(required=True)

    sample = graphene.Field(SampleType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, input, author_id):
        """新しいサンプルを作成。"""
        service = SampleService()
        try:
            sample = service.create_sample(
                author_id=author_id,
                **input.__dict__
            )
            return CreateSample(sample=sample, success=True, message='サンプルが正常に作成されました')
        except Exception as e:
            return CreateSample(sample=None, success=False, message=str(e))

class UpdateSample(graphene.Mutation):
    """サンプルを更新するミューテーション。"""
    class Arguments:
        id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)
        input = SampleUpdateInput(required=True)
        is_staff = graphene.Boolean(default_value=False)

    sample = graphene.Field(SampleType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, user_id, input, is_staff=False):
        """サンプルを更新。"""
        service = SampleService()
        try:
            sample = service.update_sample(
                sample_id=id,
                user_id=user_id,
                is_staff=is_staff,
                **input.__dict__
            )
            return UpdateSample(sample=sample, success=True, message='サンプルが正常に更新されました')
        except Exception as e:
            return UpdateSample(sample=None, success=False, message=str(e))

class DeleteSample(graphene.Mutation):
    """サンプルを削除するミューテーション。"""
    class Arguments:
        id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)
        is_staff = graphene.Boolean(default_value=False)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, user_id, is_staff=False):
        """サンプルを削除。"""
        service = SampleService()
        try:
            service.delete_sample(sample_id=id, user_id=user_id, is_staff=is_staff)
            return DeleteSample(success=True, message='サンプルが正常に削除されました')
        except Exception as e:
            return DeleteSample(success=False, message=str(e))