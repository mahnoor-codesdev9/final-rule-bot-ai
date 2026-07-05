"""
Application chat service.

The service is the web API's single coordination point for the rule matcher,
optional AI providers, persistent history, and in-process statistics.
"""

from __future__ import annotations

from dataclasses import dataclass
import asyncio
from typing import Literal

from chatbot.config import UNKNOWN_RESPONSE
from chatbot.session import SessionManager
from chatbot.statistics import Statistics
from chatbot.utils import normalize_input
from core.logging import logger
from core.settings import Settings, get_settings
from llm.base import LLMError
from llm.provider_manager import LLMProviderManager
from chatbot.matcher import ResponseMatcher # Moved here to avoid circular import with responses_safe

ChatMode = Literal["rule", "ai", "auto"]


@dataclass(frozen=True)
class ChatResult:
    """
    Chat service response.
    """

    response: str
    mode: ChatMode
    provider: str | None = None
    fallback: bool = False


class ChatService:
    """
    Coordinate responses and web chat state.
    """

    def __init__(
        self,
        settings: Settings | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.matcher = ResponseMatcher()
        self.session = SessionManager(self.settings.history_path)
        self.statistics = Statistics()
        self.llm = LLMProviderManager(self.settings)

    async def get_response(
        self,
        message: str,
        mode: ChatMode = "rule",
        provider: str | None = None,
    ) -> ChatResult:
        """
        Generate and persist a chatbot response.
        """
        normalized_message = normalize_input(message)

        if not normalized_message:
            return ChatResult(response=UNKNOWN_RESPONSE, mode="rule")

        selected_mode = self._resolve_mode(mode)
        result = await self._generate(normalized_message, selected_mode, provider)

        self.session.append(
            "user",
            normalized_message,
            mode=result.mode,
            provider=result.provider,
        )
        self.session.append(
            "bot",
            result.response,
            mode=result.mode,
            provider=result.provider,
        )
        self.statistics.user_message()
        self.statistics.bot_message(result.mode, result.fallback)

        return result

    def history(self) -> list[dict]:
        """
        Return persistent conversation history.
        """
        return self.session.load()

    def clear(self) -> None:
        """
        Clear persistent history and active stats.
        """
        self.session.clear()
        self.statistics.reset()

    def stats(self) -> dict[str, int]:
        """
        Return active process statistics.
        """
        return self.statistics.to_dict()

    def public_settings(self) -> dict:
        """
        Return frontend-safe settings and provider availability.
        """
        return {
            "app_name": self.settings.app_name,
            "version": self.settings.app_version,
            "environment": self.settings.environment,
            "default_mode": self.settings.default_mode,
            "ai_enabled": self.llm.has_available_provider(),
            "providers": self.llm.availability(),
            "max_message_length": self.settings.max_message_length,
        }

    def _resolve_mode(
        self,
        mode: ChatMode,
    ) -> ChatMode:
        """
        Resolve requested mode against deployment capabilities.
        """
        if mode == "auto":
            return "ai" if self.llm.has_available_provider() else "rule"

        if mode == "ai" and not self.llm.has_available_provider():
            return "rule"

        return mode

    async def _generate(
        self,
        message: str,
        mode: ChatMode,
        provider: str | None,
    ) -> ChatResult:
        """
        Generate from AI when possible, otherwise use rule-based matching.
        """
        # Always attempt a rule-based match first to preserve deterministic
        # behavior and avoid unnecessary AI calls.
        match = self.matcher.match(message)

        # If we have a confident rule match, return it.
        if match.response and match.confidence >= self.matcher.MEDIUM_CONFIDENCE:
            return ChatResult(response=match.response, mode="rule", provider=None, fallback=False)

        # If mode explicitly requests AI, or no good rule match exists and AI
        # is available (prefer Gemini when configured), route to the LLM.
        use_ai = mode == "ai" or (
            not match.response and bool(self.settings.gemini_api_key)
            and self.llm.has_available_provider() # Ensure AI is actually available
        )

        if use_ai:
            # Prefer Gemini specifically if a key is present and no provider
            # was explicitly requested.
            selected_provider = provider or ("gemini" if self.settings.gemini_api_key else None)

            try:
                result = await self.llm.generate(message, selected_provider)
                return ChatResult(response=result.text, mode="ai", provider=result.provider, fallback=False)
            except LLMError as error:
                logger.warning("AI request failed, falling back to rules: %s", error)
                # Fall through to rule-based behavior below.

        # If AI was not used or it failed, rely on the matcher's robust find_response.
        # This method already handles suggestions and the UNKNOWN_RESPONSE.
        final_response = self.matcher.find_response(message)
        return ChatResult(response=final_response, mode="rule", provider=None, fallback=(final_response == UNKNOWN_RESPONSE))

    def responses_safe(self, key: str) -> str:
        """Return a response by key safely falling back to UNKNOWN_RESPONSE."""
        return self.matcher.find_response(key) if key else UNKNOWN_RESPONSE

    def _rule_response(
        self,
        message: str,
    ) -> str:
        """
        Generate a deterministic rule-based response.
        """
        response = self.matcher.find_response(message)
        return response or UNKNOWN_RESPONSE
