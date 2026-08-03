from groq import Groq

from app.core.config import settings
from app.core.constants import (
    MAX_ARTICLE_INPUT_LENGTH,
    GROQ_MODEL,
    SUMMARY_TEMPERATURE,
    CHAT_TEMPERATURE,
    
)
from app.services.llm.prompts import (
    ARTICLE_SUMMARY_PROMPT,
    CLUSTER_SUMMARY_PROMPT,
    CHAT_SYSTEM_PROMPT,
)


class GroqService:

    def __init__(self):
        self.client = Groq(
            api_key=settings.groq_api_key
        )

    def generate_summary(
        self,
        article_content: str,
    ) -> str:

        article_content = article_content[:MAX_ARTICLE_INPUT_LENGTH]

        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": ARTICLE_SUMMARY_PROMPT,
                },
                {
                    "role": "user",
                    "content": article_content,
                },
            ],
            temperature=SUMMARY_TEMPERATURE,
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
        text: str,
    ) -> str:

        text = text[:MAX_ARTICLE_INPUT_LENGTH]

        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": CLUSTER_SUMMARY_PROMPT,
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
            temperature=SUMMARY_TEMPERATURE,
        )

        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

    def generate_chat_completion(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": CHAT_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=CHAT_TEMPERATURE,
        )

        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )