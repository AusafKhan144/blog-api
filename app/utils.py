from app.schemas.article import ArticleCreate
from app.models.tags import Tags, ArticleTags
from sqlalchemy.orm import Session


def handle_article_tags(
    db: Session, article_id: int, tag_names: list[str], replace: bool = True
) -> list[str]:
    tag_names_set = set(tag_names)

    # Get existing tags from DB
    existing_tags = db.query(Tags).filter(Tags.name.in_(tag_names_set)).all()
    existing_tag_names = {tag.name for tag in existing_tags}
    new_tag_names = tag_names_set - existing_tag_names

    # Create new Tags
    new_tags = [Tags(name=name) for name in new_tag_names]
    db.add_all(new_tags)
    db.flush()

    all_tags = existing_tags + new_tags

    if replace:
        # Remove existing tag relationships
        db.query(ArticleTags).filter(ArticleTags.article_id == article_id).delete()

    # Add only new relationships
    existing_tag_ids = {
        at.tag_id
        for at in db.query(ArticleTags)
        .filter(ArticleTags.article_id == article_id)
        .all()
    }

    new_relations = [
        ArticleTags(article_id=article_id, tag_id=tag.id)
        for tag in all_tags
        if tag.id not in existing_tag_ids
    ]
    db.add_all(new_relations)

    # Final list of tag names after update
    return [tag.name for tag in all_tags]


def object_to_dict(obj):
    """Convert an SQLAlchemy model object to a dictionary."""
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
