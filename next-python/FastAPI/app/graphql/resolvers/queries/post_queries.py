# This file contains post-related queries extracted from 'queries.py'.
# Add the relevant code here.

import strawberry

@strawberry.type
class Post:
    id: int
    title: str
    content: str

@strawberry.field
def get_post(post_id: int) -> Post:
    # 実際のロジックをここに記述
    return Post(id=post_id, title="Sample Title", content="Sample Content")