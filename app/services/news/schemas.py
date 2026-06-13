from dataclasses import dataclass

@dataclass
class ParsedArticle:
    title: str
    content: str
    source: str
    url: str
    published_at: str | None