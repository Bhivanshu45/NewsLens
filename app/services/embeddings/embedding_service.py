from sentence_transformers import SentenceTransformer

from app.db.models.article import Article
from app.core.constants import EMBEDDING_MODEL


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def generate_article_embedding(
        self,
        article: Article,
    ) -> list[float]:

        text = f"""
Title:
{article.title}

Summary:
{article.summary or ""}

Content:
{article.content}
"""

        return self.generate_embedding(text)