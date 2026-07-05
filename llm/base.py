"""
Shared LLM client primitives.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx


class LLMError(RuntimeError):
    """Raised when an optional AI provider cannot generate a response."""


@dataclass(frozen=True)
class LLMResult:
    """Provider response."""

    text: str
    provider: str


class HttpLLMClient:
    """Async HTTP client for JSON AI APIs using httpx."""

    provider: str

    async def _post_json(
        self,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any],
        timeout: int,
    ) -> dict[str, Any]:
        """POST JSON and return a decoded JSON object asynchronously."""
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                resp = await client.post(url, json=payload, headers={"Content-Type": "application/json", **headers})
            except httpx.HTTPStatusError as error:
                raise LLMError(f"{self.provider} request failed: {error}") from error
            except httpx.RequestError as error:
                raise LLMError(f"{self.provider} request failed: {error}") from error

        try:
            decoded = resp.json()
        except Exception as error:
            raise LLMError(f"{self.provider} returned invalid JSON.") from error

        if not isinstance(decoded, dict):
            raise LLMError(f"{self.provider} returned an invalid payload.")

        return decoded
