from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ArticleCreate(BaseModel):
    title: str
    author: str
    body: Optional[str]

    class Config:
        from_attributes = True


class ArticleResponse(BaseModel):
    id: int
    title: str
    author: str
    body: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    body: Optional[str] = None

    class Config:
        from_attributes = True
