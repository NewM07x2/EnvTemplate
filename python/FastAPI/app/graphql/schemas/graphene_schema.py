"""Graphene-based GraphQL schema configuration."""

from graphene import ObjectType, String, Schema

class Query(ObjectType):
    hello = String(description="A simple GraphQL query")

    def resolve_hello(root, info):
        return "Hello, GraphQL!"

schema = Schema(query=Query)