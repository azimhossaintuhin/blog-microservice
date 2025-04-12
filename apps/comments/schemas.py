from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class ReplyOut(BaseModel):
    id: UUID
    comment_id: UUID
    user_id: UUID
    content: str
    created_at: datetime

class CommentIn(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

class CommentOut(BaseModel):
    id: UUID
    blog_id: UUID
    user_id: UUID
    content: str
    created_at: datetime
    replies: list[ReplyOut] = []

    class Config:
        from_attributes = True

class CommentUpdateOut(BaseModel):
    id: UUID
    blog_id: UUID
    user_id: UUID
    content: str
    created_at: datetime


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

class ReplyIn(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
