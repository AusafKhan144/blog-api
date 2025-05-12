from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ArticleCreate(BaseModel):
    title: str
    author: str
    body: Optional[str]
    tags: Optional[list]

    class Config:
        from_attributes = True


class ArticleResponse(BaseModel):
    id: int
    title: str
    author: str
    body: Optional[str] = None
    tags: Optional[list]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[list]

    class Config:
        from_attributes = True
