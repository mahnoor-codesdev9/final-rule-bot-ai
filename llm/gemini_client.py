"""Google Gemini client."""

from __future__ import annotations

import asyncio
import logging

from llm.base import LLMError, LLMResult
from llm.prompts import build_prompt

try:
    import google.generativeai as generativeai
except ImportError:
    generativeai = None

logger = logging.getLogger("rulebot.llm.gemini")


class GeminiClient:
    provider = "gemini"

    def __init__(
        self,
        api_key: str | None,
        timeout: int = 30,
        retry_limit: int = 2,
        available: bool | None = None,
    ) -> None:
        self.api_key = api_key
        self.timeout = timeout
        self.retry_limit = retry_limit
        self._available_override = available

    # Support both legacy (AIza...) and newer (AQ...) API keys.
    _VALID_PREFIXES = ("AIza", "AQ.")
    _MIN_KEY_LENGTH = 30

    @property
    def _sdk_available(self) -> bool:
        return generativeai is not None

    @property
    def _has_valid_key(self) -> bool:
        if not self.api_key:
            return False

        key = self.api_key.strip()

        return (
            any(key.startswith(prefix) for prefix in self._VALID_PREFIXES)
            and len(key) >= self._MIN_KEY_LENGTH
        )

    @property
    def available(self) -> bool:
        if self._available_override is not None:
            return self._available_override

        return self._has_valid_key and self._sdk_available

    @available.setter
    def available(self, value: bool) -> None:
        self._available_override = bool(value)

    async def generate(self, prompt: str) -> LLMResult:
        if not self.api_key:
            raise LLMError("GEMINI_API_KEY is missing.")

        if not self._sdk_available:
            raise LLMError("Gemini SDK is not installed.")

        request_prompt = build_prompt(prompt)

        last_error = None

        for attempt in range(1, self.retry_limit + 1):
            try:
                response = await asyncio.wait_for(
                    asyncio.to_thread(
                        self._invoke_gemini,
                        request_prompt,
                    ),
                    timeout=self.timeout,
                )

                return LLMResult(
                    text=response,
                    provider=self.provider,
                )

            except asyncio.TimeoutError:
                last_error = LLMError("Gemini request timed out.")

            except Exception as e:
                logger.exception(e)
                last_error = LLMError(str(e))

            if attempt < self.retry_limit:
                await asyncio.sleep(2)

        raise last_error or LLMError("Gemini failed.")

    def _invoke_gemini(self, request_prompt: str) -> str:
        if generativeai is None:
            raise LLMError("Gemini SDK is not installed.")

        generativeai.configure(api_key=self.api_key)

        model = generativeai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(
            request_prompt,
            generation_config={
                "temperature": 0.4,
            },
        )

        if not getattr(response, "text", None):
            raise LLMError("Gemini returned no response.")

        return response.text.strip()