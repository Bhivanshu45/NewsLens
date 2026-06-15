from app.db.session import SessionLocal
from app.db.models.article import Article
from app.services.llm.groq_service import GroqService


def backfill_summaries():
    db = SessionLocal()
    groq_service = GroqService()

    try:
        articles = (
            db.query(Article)
            .filter(Article.summary.is_(None))
            .all()
        )

        print(
            f"Found {len(articles)} articles without summaries."
        )

        updated = 0

        for article in articles:

            try:
                summary = groq_service.generate_summary(
                    article.content
                )

                article.summary = summary

                updated += 1

                print(
                    f"[{updated}] Updated article ID={article.id}"
                )

            except Exception as e:
                print(
                    f"Failed for article ID={article.id}: {e}"
                )

        db.commit()

        print(
            f"Successfully updated {updated} articles."
        )

    finally:
        db.close()


if __name__ == "__main__":
    backfill_summaries()