import graphene
from graphene_django import DjangoObjectType
from ..models.about_model import About
from ..service.about_service import AboutService

class AboutType(DjangoObjectType):
    """AboutモデルのGraphQLタイプ。"""
    class Meta:
        model = About
        fields = ['id', 'context', 'created_at', 'updated_at']

class AboutQuery(graphene.ObjectType):
    aboutList = graphene.List(AboutType)
    aboutItem = graphene.Field(AboutType, id=graphene.Int(required=True))

    def resolve_categories(self, info):
        """全てのAboutを取得。"""
        service = AboutService()
        return service.get_abouts()

    def resolve_aboutItem(self, info, id):
        """IDでAboutを取得。"""
        service = AboutService()
        return service.get_about(id=id)