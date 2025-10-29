"""Sample GraphQL schema."""

import strawberry

@strawberry.type
class Sample:
    id: int
    name: str

@strawberry.type
class Query:
    @strawberry.field
    def get_sample(self, id: int) -> Sample:
        return Sample(id=id, name="Sample Name")