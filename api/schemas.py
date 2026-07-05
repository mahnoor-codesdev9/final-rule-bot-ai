"""
Pydantic schemas for the RuleBot AI API.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

ChatMode = Literal["rule", "ai", "auto"]
AIProvider = Literal["gemini", "groq", "openrouter"]


class ChatRequest(BaseModel):
    """
    User chat request.
    """

    message: str = Field(
        min_length=1,
        max_length=4000,
    )
    mode: ChatMode = "rule"
    provider: AIProvider | None = None
    voice_output: bool = False

    @field_validator("message")
    @classmethod
    def clean_message(cls, value: str) -> str:
        """
        Reject messages that are only whitespace.
        """
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Message cannot be empty.")

        return cleaned


class ChatResponse(BaseModel):
    """
    Chat response payload.
    """

    response: str
    mode: ChatMode
    provider: str | None = None
    fallback: bool = False


class HistoryItem(BaseModel):
    """
    One saved chat history item.
    """

    sender: str
    message: str
    mode: str = "rule"
    provider: str | None = None
    timestamp: str | None = None


class HistoryResponse(BaseModel):
    """
    Saved chat history payload.
    """

    history: list[HistoryItem]


class StatsResponse(BaseModel):
    """
    Session statistics.
    """

    user_messages: int
    bot_messages: int
    total_messages: int
    session_seconds: int
    rule_responses: int
    ai_responses: int
    fallbacks: int


class SettingsResponse(BaseModel):
    """
    Frontend-safe runtime settings.
    """

    app_name: str
    version: str
    environment: str
    default_mode: str
    ai_enabled: bool
    providers: dict[str, bool]
    max_message_length: int


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str
    app: str
    version: str


class StatusResponse(BaseModel):
    """
    Generic success response.
    """

    status: str
