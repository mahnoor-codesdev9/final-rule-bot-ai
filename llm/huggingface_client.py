"""
Legacy Hugging Face client.

Hugging Face is not part of the current UI provider list, but this module stays
import-safe for existing code that may reference it.
"""

from __future__ import annotations

from llm.base import LLMError, LLMResult


class HuggingFaceClient:
    """
    Disabled legacy provider.
    """

    provider = "huggingface"
    available = False

    async def generate(
        self,
        prompt: str,
    ) -> LLMResult:
        """
        Raise a clear error instead of crashing on missing dependencies.
        """
        raise LLMError("Hugging Face provider is not configured.")
