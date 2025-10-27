"""GraphQL schema configuration."""

import graphene
# from apps.users.schema import UserQuery, UserMutation
# from apps.posts.schema import PostQuery, PostMutation


class Query(graphene.ObjectType):
    """Root Query for GraphQL API."""
    pass


class Mutation(graphene.ObjectType):
    """Root Mutation for GraphQL API."""
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
