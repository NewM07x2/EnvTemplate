# This file contains post-related mutations extracted from 'mutations.py'.
# Add the relevant code here.

import strawberry

@strawberry.mutation
def create_post(title: str, content: str) -> str:
    # 実際のロジックをここに記述
    return f"Post '{title}' created successfully!"