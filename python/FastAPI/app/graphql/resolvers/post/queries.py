from typing import List, Optional
import strawberry
from strawberry.types import Info
from app.core.database import prisma
from app.graphql.types import Post

@strawberry.type
class PostQueries:
    @strawberry.field
    async def posts(self, info: Info) -> List[Post]:
        posts = await prisma.post.find_many()
        return [
            Post(
                id=post.id,
                title=post.title,
                content=post.content,
                published=post.published,
                author_id=post.authorid,
                created_at=post.createdat,
                updated_at=post.updatedat,
            )
            for post in posts
        ]

    @strawberry.field
    async def post(self, info: Info, id: str) -> Optional[Post]:
        post = await prisma.post.find_unique(where={"id": id})
        if not post:
            return None
        return Post(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            author_id=post.authorid,
            created_at=post.createdat,
            updated_at=post.updatedat,
        )