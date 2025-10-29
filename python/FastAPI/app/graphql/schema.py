"""GraphQL schema configuration."""

import strawberry
from graphene import ObjectType, String, Schema
from app.graphql.resolvers import Mutation, Query
from app.graphql.resolvers.mutations.post_mutations import create_post
from app.graphql.resolvers.mutations.user_mutations import create_user
from app.graphql.resolvers.queries.post_queries import get_post
from app.graphql.resolvers.queries.user_queries import get_user

# Graphene-based schema
class GrapheneQuery(ObjectType):
    hello = String(description="A simple GraphQL query")

    def resolve_hello(root, info):
        return "Hello, GraphQL!"

graphene_schema = Schema(query=GrapheneQuery)

# Strawberry-based schema
@strawberry.type
class Query:
    get_post = get_post
    get_user = get_user

@strawberry.type
class Mutation:
    create_post = create_post
    create_user = create_user

strawberry_schema = strawberry.Schema(query=Query, mutation=Mutation)
