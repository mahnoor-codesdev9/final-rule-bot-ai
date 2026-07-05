"""
OpenAI-compatible chat completion client.

This class is kept for backwards compatibility with existing imports. RuleBot
AI now uses `OpenRouterClient` and `GroqClient` for optional SaaS AI mode.
"""

from __future__ import annotations

from llm.openrouter_client import OpenRouterClient


class OpenAIClient(OpenRouterClient):
    """
    Backwards-compatible alias for an OpenAI-compatible endpoint.
    """
