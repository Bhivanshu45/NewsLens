# Responsibility:

# Take Parsed Articles
# Check Duplicates
# Store In PostgreSQL

# No RSS parsing.

from app.services.news.rss_service import RSSService
from sqlalchemy.orm import Session
from app.db.models.article import Article

class NewsService:
    def __init__(self):
        self.rss_service = RSSService()

    def ingest_articles(self, db:Session):
        articles = self.rss_service.fetch_and_parse_feeds()

        inserted = 0
        skipped = 0

        for article in articles:
            existing_article = (
                db.query(Article)
                .filter(Article.url == article.url)
                .first()
            )

            if existing_article:
                skipped += 1
                continue

            article_data = Article(
                title=article.title,
                content=article.content,
                source=article.source,
                url=article.url,
                published_at=None
            )

            db.add(article_data)

            inserted += 1

        db.commit()

        return {
            "fetched": len(articles),
            "inserted": inserted,
            "skipped": skipped,
        }