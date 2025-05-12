from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class Tags(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    article_tags = relationship("ArticleTags", back_populates="tag")


class ArticleTags(Base):
    __tablename__ = 'article_tags'

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("article.id",ondelete='CASCADE'), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id",ondelete='CASCADE'), nullable=False)

    tag = relationship("Tags", back_populates="article_tags")
    article = relationship("Article", back_populates="article_tags")
