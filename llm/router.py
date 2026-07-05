"""Optional AI provider router.

The router registers only clients declared in `Settings.allowed_ai_providers`.
This keeps provider discovery deterministic and prevents exposing
unconfigured provider names to the frontend.
"""

from __future__ import annotations

from core.settings import Settings, get_settings
from llm.base import LLMError, LLMResult
from llm.gemini_client import GeminiClient
from llm.groq_client import GroqClient
from llm.openrouter_client import OpenRouterClient


class LLMRouter:
    """Select and call the configured optional AI provider."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.clients: dict[str, object] = {}

        # Register only allowed providers. The concrete client may still be
        # marked unavailable if the API key is missing; availability() hides
        # keys and only reports readiness booleans.
        for name in self.settings.allowed_ai_providers:
            if name == "gemini":
                self.clients["gemini"] = GeminiClient(
                    self.settings.gemini_api_key,
                    self.settings.request_timeout,
                )
            elif name == "groq":
                self.clients["groq"] = GroqClient(
                    self.settings.groq_api_key,
                    self.settings.request_timeout,
                )
            elif name == "openrouter":
                self.clients["openrouter"] = OpenRouterClient(
                    self.settings.openrouter_api_key,
                    self.settings.request_timeout,
                )

    def availability(self) -> dict[str, bool]:
        """Return provider availability without exposing secrets."""
        return {
            name: getattr(client, "available", False)
            for name, client in self.clients.items()
        }

    def has_available_provider(self) -> bool:
        """Return whether any provider can be used."""
        return any(self.availability().values())

    async def generate(self, prompt: str, provider: str | None = None) -> LLMResult:
        """Generate a response from the selected provider asynchronously."""
        selected = provider or self._first_available_provider()

        if selected not in self.clients:
            raise LLMError(f"Unsupported AI provider: {selected}")

        client = self.clients[selected]

        if not getattr(client, "available", False):
            raise LLMError(f"{selected} is not configured.")

        return await client.generate(prompt)

    def _first_available_provider(self) -> str:
        """Return the first configured provider."""
        for name, available in self.availability().items():
            if available:
                return name

        raise LLMError("No AI provider is configured.")
