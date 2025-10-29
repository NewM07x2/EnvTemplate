"""User GraphQL schema."""

import strawberry

@strawberry.type
class User:
    id: int
    username: str

@strawberry.type
class Query:
    @strawberry.field
    def get_user(self, id: int) -> User:
        return User(id=id, username="User Name")