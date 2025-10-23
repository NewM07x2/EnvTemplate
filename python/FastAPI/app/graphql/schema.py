"""GraphQL schema configuration."""

import strawberry

from app.graphql.resolvers import Mutation, Query

# Create GraphQL schema
graphql_schema = strawberry.Schema(query=Query, mutation=Mutation)
