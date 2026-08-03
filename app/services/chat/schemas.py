from enum import Enum

from pydantic import BaseModel, Field


class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatRequest(BaseModel):
    query: str
    conversation_id: str | None = None


class ChatMessage(BaseModel):
    role: ChatRole
    content: str


class SourceReference(BaseModel):
    title: str
    source: str
    url: str


class ConversationHistory(BaseModel):
    messages: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    sources: list[SourceReference] = Field(default_factory=list)
