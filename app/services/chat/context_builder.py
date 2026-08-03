from app.services.chat.schemas import ChatMessage
from app.services.chat.schemas import ChatRole
from app.services.chat.schemas import ConversationHistory
from app.services.retrieval.schemas import RetrievedArticle


class ContextBuilder:
    _divider = "----------------------------------------------------"

    def build_context(
        self,
        history: ConversationHistory,
        retrieved_articles: list[RetrievedArticle],
    ) -> str:
        sections = [
            self._build_system_prompt(),
            self._divider,
        ]

        history_section = self._build_history(history)
        if history_section:
            sections.extend([
                history_section,
                self._divider,
            ])

        sections.extend([
            self._build_articles(retrieved_articles),
        ])

        return "\n\n".join(sections)

    def _build_system_prompt(self) -> str:
        return (
            "SYSTEM INSTRUCTION\n\n"
            "You are NewsLens AI, an intelligent news assistant.\n\n"
            "Answer ONLY using the retrieved news articles provided below.\n\n"
            "Do not use outside knowledge.\n\n"
            "If the answer cannot be determined from the provided articles, clearly say that you do not have enough information.\n\n"
            "Never hallucinate facts.\n\n"
            "When relevant, mention the source name while answering."
        )

    def _build_history(self, history: ConversationHistory) -> str:
        if not history.messages:
            return ""

        lines = ["CONVERSATION HISTORY", ""]
        for message in history.messages:
            lines.append(f"{self._format_role(message.role)}: {message.content}")

        return "\n".join(lines).rstrip()

    def _build_articles(self, retrieved_articles: list[RetrievedArticle]) -> str:
        lines = ["RETRIEVED ARTICLES", "", "Relevant Articles", ""]

        for index, retrieved_article in enumerate(retrieved_articles, start=1):
            article = retrieved_article.article
            lines.extend([
                f"Article {index}",
                "",
                f"Title: {self._safe_text(article.title)}",
                f"Summary: {self._safe_text(article.summary)}",
                f"Source: {self._safe_text(article.source)}",
                f"Published: {self._format_published_at(article.published_at)}",
                f"URL: {self._safe_text(article.url)}",
                "",
            ])

        return "\n".join(lines).rstrip()

    def _format_role(self, role: ChatRole) -> str:
        if role == ChatRole.USER:
            return "User"
        if role == ChatRole.ASSISTANT:
            return "Assistant"
        return "System"

    def _format_published_at(self, published_at) -> str:
        if published_at is None:
            return "Unknown"

        if hasattr(published_at, "isoformat"):
            return published_at.isoformat()

        return str(published_at)

    def _safe_text(self, value: str | None) -> str:
        return value if value is not None else "Unknown"
