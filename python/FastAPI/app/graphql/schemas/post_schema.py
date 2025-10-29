"""Post GraphQL schema."""

import strawberry

@strawberry.type
class Post:
    id: int
    title: str
    content: str

@strawberry.type
class Query:
    @strawberry.field
    def get_post(self, id: int) -> Post:
        return Post(id=id, title="Sample Title", content="Sample Content")

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_post(self, title: str, content: str) -> str:
        return f"Post '{title}' created successfully!"