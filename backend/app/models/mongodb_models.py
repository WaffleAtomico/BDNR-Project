from datetime import datetime
from typing import List

from pydantic import BaseModel


class Pin(BaseModel):
    pin_id: str
    title: str
    description: str
    url: str
    tags: List[str]
    author_id: str
    created_at: datetime
    size_bytes: int = 0
    save_count: int = 0


class Board(BaseModel):
    board_id: str
    title: str
    description: str
    tags: List[str]
    author_id: str
    created_at: datetime


class Comment(BaseModel):
    comment_id: str
    pin_id: str
    user_id: str
    text: str
    created_at: datetime
