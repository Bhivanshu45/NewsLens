from sqlalchemy.orm import Session

from app.db.models.article import Article
from app.services.news.schemas import ParsedArticle


class ArticleRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        article_id: int,
    ) -> Article | None:

        return (
            self.db.query(Article)
            .filter(Article.id == article_id)
            .first()
        )

    def get_by_url(
        self,
        url: str,
    ) -> Article | None:

        return (
            self.db.query(Article)
            .filter(Article.url == url)
            .first()
        )

    def create(
        self,
        article: Article,
    ) -> Article:

        self.db.add(article)
        self.db.flush()

        return article

    def create_from_parsed_article(
        self,
        article: ParsedArticle,
        summary: str | None,
    ) -> Article:
        db_article = Article(
            title=article.title,
            content=article.content,
            summary=summary,
            source=article.source,
            url=article.url,
            published_at=article.published_at,
        )

        return self.create(db_article)

    def list_all(self) -> list[Article]:
        return (
            self.db.query(Article)
            .order_by(Article.published_at.desc())
            .all()
        )

    def list_unclustered(self) -> list[Article]:
        return (
            self.db.query(Article)
            .filter(Article.cluster_id.is_(None))
            .order_by(Article.published_at.desc())
            .all()
        )

    def assign_cluster(
        self,
        article: Article,
        cluster_id: int,
    ) -> None:

        article.cluster_id = cluster_id

    def list_articles(
        self,
        page: int,
        limit: int,
        source: str | None,
    ) -> list[Article]:
        offset = (page - 1) * limit

        query = self.db.query(Article)

        if source:
            query = query.filter(
                Article.source == source
            )

        return (
            query.order_by(
                Article.published_at.desc()
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

    def search(
        self,
        query: str,
        page: int,
        limit: int,
    ) -> list[Article]:

        offset = (page - 1) * limit

        return (
            self.db.query(Article)
            .filter(
                Article.title.ilike(
                    f"%{query}%"
                )
            )
            .order_by(
                Article.published_at.desc()
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_by_ids(
        self,
        ids: list[int],
    ) -> list[Article]:

        return (
            self.db.query(Article)
            .filter(
                Article.id.in_(ids)
            )
            .all()
        )


    def exists(
        self,
        url: str,
    ) -> bool:

        return (
            self.db.query(Article.id)
            .filter(Article.url == url)
            .first()
        is not None
        )


    def update_cluster(
        self,
        article: Article,
        cluster_id: int,
    ) -> None:
        article.cluster_id = cluster_id

    def clear_clusters(self) -> int:
        return (
            self.db.query(Article)
            .update({Article.cluster_id: None})
        )