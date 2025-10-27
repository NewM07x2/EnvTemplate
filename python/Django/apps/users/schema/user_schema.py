import graphene
from graphene_django.types import DjangoObjectType
from ..models.user_model import User

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int())

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(pk=id)