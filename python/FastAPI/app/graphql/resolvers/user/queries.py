from typing import List, Optional
import strawberry
from strawberry.types import Info
from app.core.database import prisma
from app.graphql.types import User

@strawberry.type
class UserQueries:
    @strawberry.field
    async def users(self, info: Info) -> List[User]:
        users = await prisma.user.find_many()
        return [
            User(
                id=user.id,
                email=user.email,
                username=user.username,
                first_name=user.firstname,
                last_name=user.lastname,
                is_active=user.isactive,
                created_at=user.createdat,
                updated_at=user.updatedat,
            )
            for user in users
        ]

    @strawberry.field
    async def user(self, info: Info, id: str) -> Optional[User]:
        user = await prisma.user.find_unique(where={"id": id})
        if not user:
            return None
        return User(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.firstname,
            last_name=user.lastname,
            is_active=user.isactive,
            created_at=user.createdat,
            updated_at=user.updatedat,
        )