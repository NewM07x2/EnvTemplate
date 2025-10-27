from typing import List, Optional
import strawberry
from strawberry.types import Info
from app.core.database import prisma
from app.graphql.types import Post

@strawberry.type
class PostQueries:
    """Post に関連する GraphQL クエリ

    投稿データを取得するためのクエリを提供します。
    """

    @strawberry.field
    async def posts(self, info: Info) -> List[Post]:
        """すべての投稿を取得するクエリ

        データベースからすべての投稿を取得し、Post 型のリストとして返します。
        """
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
        """特定の投稿を取得するクエリ

        指定された ID に基づいて投稿を検索し、見つからない場合は None を返します。
        """
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