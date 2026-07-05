"""
OpenRouter client.
"""

from __future__ import annotations

from llm.base import HttpLLMClient, LLMError, LLMResult


class OpenRouterClient(HttpLLMClient):
    """
    OpenRouter OpenAI-compatible chat completions client.
    """

    provider = "openrouter"

    def __init__(
        self,
        api_key: str | None = None,
        timeout: int = 30,
    ) -> None:
        self.api_key = api_key
        self.timeout = timeout

    @property
    def available(self) -> bool:
        """
        Return whether the provider has credentials.
        """
        return bool(self.api_key)

    async def generate(
        self,
        prompt: str,
    ) -> LLMResult:
        """
        Generate text through OpenRouter.
        """
        if not self.api_key:
            raise LLMError("OPENROUTER_API_KEY is missing.")
        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are RuleBot AI, a concise assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.4,
        }
        data = await self._post_json(
            "https://openrouter.ai/api/v1/chat/completions",
            {"Authorization": f"Bearer {self.api_key}"},
            payload,
            self.timeout,
        )
        text = self._extract_text(data)
        return LLMResult(text=text, provider=self.provider)

    def _extract_text(
        self,
        data: dict,
    ) -> str:
        """
        Extract text from an OpenAI-compatible payload.
        """
        try:
            text = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as error:
            raise LLMError("OpenRouter returned no text.") from error

        return str(text).strip()
