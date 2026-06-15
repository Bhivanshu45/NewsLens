from sqlalchemy.orm import Session

from app.db.models.article import Article
from app.services.news.rss_service import RSSService
from app.services.llm.groq_service import GroqService


class NewsService:
    def __init__(self, db: Session):
        self.db = db
        self.rss_service = RSSService()
        self.groq_service = GroqService()

    def ingest_articles(self):
        articles = self.rss_service.fetch_and_parse_feeds()

        inserted = 0
        skipped = 0

        for article in articles:
            existing_article = (
                self.db.query(Article)
                .filter(Article.url == article.url)
                .first()
            )

            if existing_article:
                skipped += 1
                continue

            summary = None
            print(f"Generating summary for: {article.title}")

            try:
                if article.content:
                    summary = (
                        self.groq_service
                        .generate_summary(
                            article.content
                        )
                    )

            except Exception as e:
                print(f"Summary generation failed: {e}")

            article_data = Article(
                title=article.title,
                content=article.content,
                summary=summary,
                source=article.source,
                url=article.url,
                published_at=article.published_at,
            )

            self.db.add(article_data)

            inserted += 1

        self.db.commit()

        return {
            "fetched": len(articles),
            "inserted": inserted,
            "skipped": skipped,
        }

    def get_articles(
        self,
        page: int = 1,
        limit: int = 20,
        source: str | None = None,
    ):
        offset = (page - 1) * limit

        query = self.db.query(Article)

        if source:
            query = query.filter(
                Article.source == source
            )

        return (
            query
            .order_by(Article.published_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_article_by_id(
        self,
        article_id: int,
    ):
        return (
            self.db.query(Article)
            .filter(Article.id == article_id)
            .first()
        )

    def search_articles(
        self,
        query: str,
        page: int = 1,
        limit: int = 20,
    ):
        offset = (page - 1) * limit

        return (
            self.db.query(Article)
            .filter(
                Article.title.ilike(f"%{query}%")
            )
            .order_by(Article.published_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )