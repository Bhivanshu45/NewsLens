from app.db.session import SessionLocal
from app.db.models.article import Article

db = SessionLocal()

try:
    updated = (
        db.query(Article)
        .update(
            {Article.summary: None},
            synchronize_session=False
        )
    )

    db.commit()

    print(f"Reset {updated} summaries")

finally:
    db.close()