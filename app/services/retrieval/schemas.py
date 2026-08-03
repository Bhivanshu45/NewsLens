from dataclasses import dataclass

from app.db.models.article import Article


@dataclass
class RetrievedArticle:
    article: Article
    score: float