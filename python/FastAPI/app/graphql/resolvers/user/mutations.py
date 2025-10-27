from typing import Optional
import strawberry
from strawberry.types import Info
from app.core.database import prisma
from app.graphql.types import User, UserCreateInput, UserUpdateInput
from app.core.security import get_password_hash

@strawberry.type
class UserMutations:
    @strawberry.mutation
    async def create_user(self, info: Info, input: UserCreateInput) -> User:
        user = await prisma.user.create(
            data={
                "email": input.email,
                "username": input.username,
                "password": get_password_hash(input.password),
                "firstname": input.first_name,
                "lastname": input.last_name,
            }
        )
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

    @strawberry.mutation
    async def update_user(self, info: Info, id: str, input: UserUpdateInput) -> Optional[User]:
        update_data = {}
        if input.email is not None:
            update_data["email"] = input.email
        if input.username is not None:
            update_data["username"] = input.username
        if input.first_name is not None:
            update_data["firstname"] = input.first_name
        if input.last_name is not None:
            update_data["lastname"] = input.last_name
        if input.is_active is not None:
            update_data["isactive"] = input.is_active
        if not update_data:
            return None
        user = await prisma.user.update(where={"id": id}, data=update_data)
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

    @strawberry.mutation
    async def delete_user(self, info: Info, id: str) -> bool:
        try:
            await prisma.user.delete(where={"id": id})
            return True
        except Exception:
            return False