from groq import Groq

from app.core.config import settings


class GroqService:

    def __init__(self):
        self.client = Groq(
            api_key=settings.groq_api_key
        )

    def generate_summary(
        self,
        article_content: str
    ) -> str:

        article_content = article_content[:8000]

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a professional news summarizer.

Your task is to summarize the article provided by the user.

Rules:
- Never say you cannot verify information.
- Never ask for more context.
- Never mention being an AI assistant.
- Never refuse.
- Generate exactly 3-4 factual sentences.
- Use only the information present in the article.
- Return only the summary.
"""
                },
                {
                    "role": "user",
                    "content": article_content[:8000]
                }
            ],
            temperature=0.1,
        )

        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )
    

    def generate_cluster_summary(
        self,
        text: str
    ) -> str:

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
    Summarize the common event/topic covered by these news articles.
    Return only 3-4 concise sentences.
    """
                }    ,
                {
                    "role": "user",
                    "content": text[:8000]
                }
            ],
            temperature=0.1,
        )

        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )