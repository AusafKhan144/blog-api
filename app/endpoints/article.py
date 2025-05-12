from datetime import datetime
from typing import Optional
from app.models.tags import ArticleTags, Tags
from app.schemas.article import ArticleCreate, ArticleResponse, ArticleUpdate
from app.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from app.models.article import Article
from app.utils import handle_article_tags, object_to_dict
from fastapi import Query

router = APIRouter(prefix="/api/article", tags=["Article"])


@router.post("/", response_model=ArticleResponse)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    article_data = Article(**article.model_dump(exclude={"tags"}))
    db.add(article_data)
    db.flush()  # After creating article
    final_tag_names = handle_article_tags(
        db, article_id=article_data.id, tag_names=article.tags, replace=True
    )
    db.commit()

    return {**object_to_dict(article_data), "tags": final_tag_names}



@router.get("/", response_model=Page[ArticleResponse])
def get_all_articles(
    db: Session = Depends(get_db),
    tag: Optional[list[str]] = Query(default=None),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    article_filters = []

    if start_date:
        article_filters.append(Article.created_at >= start_date)
    if end_date:
        article_filters.append(Article.created_at <= end_date)

    query = db.query(Article)

    if tag:
        query = query.join(ArticleTags).join(Tags).filter(Tags.name.in_(tag))

    if article_filters:
        query = query.filter(*article_filters)

    articles = query.all()
    response = []

    for art in articles:
        tag_names = [
            t.name for t in db.query(Tags)
            .join(ArticleTags, Tags.id == ArticleTags.tag_id)
            .filter(ArticleTags.article_id == art.id)
            .all()
        ]
        response.append({**object_to_dict(art), "tags": tag_names})

    return paginate(response)



@router.get("/{id}", response_model=ArticleResponse)
def get_article_by_id(id: int, db: Session = Depends(get_db)):
    article_data = db.query(Article).filter(Article.id == id).first()
    tag_names = [
        tag.name
        for tag in db.query(Tags)
        .join(ArticleTags, Tags.id == ArticleTags.tag_id)
        .filter(ArticleTags.article_id == id)
        .all()
    ]

    if not article_data:
        raise HTTPException(404, f"Article id {id} Not Found")

    return {**object_to_dict(article_data), "tags": tag_names}


@router.put("/{id}", response_model=ArticleResponse)
def update_article(id: int, article: ArticleUpdate, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")

    for key, value in article.model_dump(exclude={"tags"}).items():
        setattr(db_article, key, value)

    db.flush()
    if article.tags is not None:
        final_tag_names = handle_article_tags(
            db, article_id=id, tag_names=article.tags, replace=True
        )

    db.commit()
    db.refresh(db_article)

    return {**object_to_dict(db_article), "tags": final_tag_names}


@router.patch("/{id}", response_model=ArticleResponse)
def patch_article(id: int, article: ArticleUpdate, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")

    for key, value in article.model_dump(exclude_unset=True, exclude={"tags"}).items():
        setattr(db_article, key, value)

    db.flush()
    if article.tags:
        final_tag_names = handle_article_tags(
            db, article_id=id, tag_names=article.tags, replace=False
        )

    db.commit()
    db.refresh(db_article)
    return {**object_to_dict(db_article), "tags": final_tag_names}


@router.delete("/{id}")
def delete_article_by_id(id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == id).first()
    if not db_article:
        raise HTTPException(404, f"Article id {id} Not Found")

    db.delete(db_article)
    db.commit()

    return {"detail": f"Article id {id} deleted sucesfully!"}
