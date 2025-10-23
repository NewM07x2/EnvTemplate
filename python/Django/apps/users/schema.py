"""User GraphQL schema.

Sample GraphQL types, queries, and mutations that can be copied and modified.
"""

import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .services import UserService

User = get_user_model()


class UserType(DjangoObjectType):
    """GraphQL type for User model."""
    
    full_name = graphene.String()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'bio', 'avatar', 'is_verified', 'is_active',
            'created_at', 'updated_at'
        ]
    
    def resolve_full_name(self, info):
        return self.full_name


class UserInput(graphene.InputObjectType):
    """Input type for creating/updating users."""
    email = graphene.String(required=True)
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    bio = graphene.String()
    avatar = graphene.String()


class UserUpdateInput(graphene.InputObjectType):
    """Input type for updating users."""
    first_name = graphene.String()
    last_name = graphene.String()
    bio = graphene.String()
    avatar = graphene.String()


class UserQuery(graphene.ObjectType):
    """User queries."""
    
    users = graphene.List(
        UserType,
        skip=graphene.Int(default_value=0),
        limit=graphene.Int(default_value=100)
    )
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    user_by_email = graphene.Field(UserType, email=graphene.String(required=True))
    
    def resolve_users(self, info, skip=0, limit=100):
        """Get all users with pagination."""
        service = UserService()
        return service.get_users(skip=skip, limit=limit)
    
    def resolve_user(self, info, id):
        """Get user by ID."""
        service = UserService()
        return service.get_user(user_id=id)
    
    def resolve_user_by_email(self, info, email):
        """Get user by email."""
        service = UserService()
        return service.get_user_by_email(email=email)


class CreateUser(graphene.Mutation):
    """Mutation to create a new user."""
    
    class Arguments:
        input = UserInput(required=True)
    
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, input):
        """Create new user."""
        service = UserService()
        try:
            user = service.create_user(
                email=input.email,
                username=input.username,
                password=input.password,
                first_name=input.first_name,
                last_name=input.last_name,
                bio=input.get('bio'),
                avatar=input.get('avatar'),
            )
            return CreateUser(user=user, success=True, message='User created successfully')
        except Exception as e:
            return CreateUser(user=None, success=False, message=str(e))


class UpdateUser(graphene.Mutation):
    """Mutation to update a user."""
    
    class Arguments:
        id = graphene.Int(required=True)
        input = UserUpdateInput(required=True)
    
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, id, input):
        """Update user."""
        service = UserService()
        try:
            user = service.update_user(
                user_id=id,
                **input.__dict__
            )
            return UpdateUser(user=user, success=True, message='User updated successfully')
        except Exception as e:
            return UpdateUser(user=None, success=False, message=str(e))


class DeleteUser(graphene.Mutation):
    """Mutation to delete a user."""
    
    class Arguments:
        id = graphene.Int(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, id):
        """Delete user."""
        service = UserService()
        try:
            service.delete_user(user_id=id)
            return DeleteUser(success=True, message='User deleted successfully')
        except Exception as e:
            return DeleteUser(success=False, message=str(e))


class UserMutation(graphene.ObjectType):
    """User mutations."""
    
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
