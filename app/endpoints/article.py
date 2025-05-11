from app.schemas.article import ArticleCreate, ArticleResponse, ArticleUpdate
from app.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from app.models.article import Article

router = APIRouter(prefix="/api/article", tags=["Article"])


@router.post("/", response_model=ArticleResponse)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    return db_article


@router.get("/", response_model=Page[ArticleResponse])
def get_all_articles(db: Session = Depends(get_db)):
    all_articles = db.query(Article).all()
    return paginate(all_articles)


@router.get("/{id}", response_model=ArticleResponse)
def get_article_by_id(id: int, db: Session = Depends(get_db)):
    article_data = db.query(Article).filter(Article.id == id).first()
    if not article_data:
        raise HTTPException(404, f"Article id {id} Not Found")

    return article_data


@router.put("/{id}", response_model=ArticleResponse)
def update_article_by_id(
    id: int, article: ArticleUpdate, db: Session = Depends(get_db)
):
    db_article = db.query(Article).filter(Article.id == id).first()
    if not db_article:
        raise HTTPException(404, f"Article id {id} Not Found")

    for key, value in article.model_dump().items():
        setattr(db_article, key, value)

    db.commit()
    db.refresh(db_article)

    return db_article


@router.patch("/{id}", response_model=ArticleResponse)
def modify_article_by_id(
    id: int, article: ArticleUpdate, db: Session = Depends(get_db)
):
    db_article = db.query(Article).filter(Article.id == id).first()
    if not db_article:
        raise HTTPException(404, f"Article id {id} Not Found")

    for key, value in article.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)

    db.commit()
    db.refresh(db_article)

    return db_article


@router.delete("/{id}")
def delete_article_by_id(id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == id).first()
    if not db_article:
        raise HTTPException(404, f"Article id {id} Not Found")

    db.delete(db_article)
    db.commit()

    return {"detail": f"Article id {id} deleted sucesfully!"}
