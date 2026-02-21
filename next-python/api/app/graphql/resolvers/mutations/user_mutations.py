# This file contains user-related mutations extracted from 'mutations.py'.
# Add the relevant code here.

import strawberry

@strawberry.mutation
def create_user(name: str, email: str) -> str:
    # 実際のロジックをここに記述
    return f"User '{name}' created successfully!"