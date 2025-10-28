import graphene
from graphene_django import DjangoObjectType
from ..models.category_model import Category
from ..service.category_service import CategoryService

class CategoryType(DjangoObjectType):
    """カテゴリモデルのGraphQLタイプ。"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at']

class CategoryQuery(graphene.ObjectType):
    """カテゴリに関するクエリ。"""
    categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.Int(required=True))

    def resolve_categories(self, info):
        """全てのカテゴリを取得。"""
        service = CategoryService()
        return service.get_categories()

    def resolve_category(self, info, id):
        """IDでカテゴリを取得。"""
        service = CategoryService()
        return service.get_category(category_id=id)