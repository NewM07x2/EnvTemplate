# This file contains user-related queries extracted from 'queries.py'.
# Add the relevant code here.

import strawberry

@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.field
def get_user(user_id: int) -> User:
    # 実際のロジックをここに記述
    return User(id=user_id, name="Sample User", email="user@example.com")