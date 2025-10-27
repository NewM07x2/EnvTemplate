from typing import Optional
import strawberry
from strawberry.types import Info
from app.core.database import prisma
from app.graphql.types import Post, PostCreateInput, PostUpdateInput

@strawberry.type
class PostMutations:
    @strawberry.mutation
    async def create_post(self, info: Info, input: PostCreateInput) -> Post:
        post = await prisma.post.create(
            data={
                "title": input.title,
                "content": input.content,
                "published": input.published,
                "authorid": input.author_id,
            }
        )
        return Post(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            author_id=post.authorid,
            created_at=post.createdat,
            updated_at=post.updatedat,
        )

    @strawberry.mutation
    async def update_post(self, info: Info, id: str, input: PostUpdateInput) -> Optional[Post]:
        update_data = {}
        if input.title is not None:
            update_data["title"] = input.title
        if input.content is not None:
            update_data["content"] = input.content
        if input.published is not None:
            update_data["published"] = input.published
        if not update_data:
            return None
        post = await prisma.post.update(where={"id": id}, data=update_data)
        return Post(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            author_id=post.authorid,
            created_at=post.createdat,
            updated_at=post.updatedat,
        )

    @strawberry.mutation
    async def delete_post(self, info: Info, id: str) -> bool:
        try:
            await prisma.post.delete(where={"id": id})
            return True
        except Exception:
            return False