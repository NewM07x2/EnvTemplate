from graphene import ObjectType, String, Schema
import strawberry

# Graphene-based schema
class Query(ObjectType):
    hello = String(description="A simple GraphQL query")

    def resolve_hello(root, info):
        return "Hello, GraphQL!"

schema = Schema(query=Query)

# Strawberry-based schema
@strawberry.type
class Sample:
    id: int
    name: str

sample_schema = strawberry.Schema(query=Sample)