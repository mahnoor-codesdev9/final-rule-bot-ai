"""
Environment-based settings for RuleBot AI.

The project intentionally avoids requiring python-dotenv at runtime. A small
loader reads `.env` when present, while deployment platforms can inject the
same variables through their environment systems.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _load_dotenv(path: Path = Path(".env")) -> None:
    """
    Load environment variables from a .env file using python-dotenv.
    """
    if not path.exists():
        return

    load_dotenv(dotenv_path=path, override=False)


def _truthy(value: str | None, default: bool = False) -> bool:
    """
    Parse common boolean environment values.
    """
    if value is None:
        return default

    return value.lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    """
    Runtime configuration.
    """

    app_name: str
    app_version: str
    environment: str
    debug: bool
    history_path: str
    max_message_length: int
    default_mode: str
    allowed_ai_providers: tuple[str, ...]
    gemini_api_key: str | None
    groq_api_key: str | None
    openrouter_api_key: str | None
    request_timeout: int
    retry_limit: int
    cors_origins: tuple[str, ...]

    @property
    def ai_enabled(self) -> bool:
        """
        Return whether any supported AI provider has a configured key.
        """
        return any(
            [
                self.gemini_api_key,
                self.groq_api_key,
                self.openrouter_api_key,
            ]
        )


def get_settings() -> Settings:
    """
    Build settings from environment variables.
    """
    _load_dotenv()

    cors_value = os.getenv("CORS_ORIGINS", "")
    cors_origins = tuple(
        item.strip()
        for item in cors_value.split(",")
        if item.strip()
    )

    return Settings(
        app_name=os.getenv(
            "APP_NAME",
            "RuleBot AI",
        ),
        app_version=os.getenv(
            "APP_VERSION",
            "2.1.0",
        ),
        environment=os.getenv(
            "APP_ENV",
            "development",
        ),
        debug=_truthy(
            os.getenv("DEBUG"),
            default=False,
        ),
        history_path=os.getenv(
            "CHAT_HISTORY_PATH",
            "chatbot/data/chat_history.json",
        ),
        max_message_length=int(
            os.getenv("MAX_MESSAGE_LENGTH", "4000")
        ),
        default_mode=os.getenv(
            "DEFAULT_CHAT_MODE",
            "rule",
        ).lower(),
        allowed_ai_providers=(
            "gemini",
            "groq",
            "openrouter",
        ),
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        groq_api_key=os.getenv("GROQ_API_KEY"),
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
        request_timeout=int(os.getenv("AI_REQUEST_TIMEOUT", "30")),
        retry_limit=int(os.getenv("AI_RETRY_LIMIT", "2")),
        cors_origins=cors_origins,
    )
