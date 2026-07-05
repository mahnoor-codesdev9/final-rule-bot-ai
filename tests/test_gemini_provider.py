"""Tests for the Gemini provider and AI fallback behavior."""

import unittest
from unittest.mock import AsyncMock, patch

from core.settings import Settings
from llm.base import LLMError, LLMResult
from llm.provider_manager import LLMProviderManager


class TestGeminiProviderManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.settings = Settings(
            app_name="RuleBot AI",
            app_version="2.1.0",
            environment="test",
            debug=True,
            history_path="chatbot/data/chat_history.json",
            max_message_length=4000,
            default_mode="rule",
            allowed_ai_providers=("gemini",),
            gemini_api_key="fake-key",
            groq_api_key=None,
            openrouter_api_key=None,
            request_timeout=5,
            retry_limit=1,
            cors_origins=(),
        )
        self.manager = LLMProviderManager(self.settings)

    def test_provider_availability(self):
        availability = self.manager.availability()
        self.assertEqual(availability["gemini"], False)

    @patch("llm.gemini_client.GeminiClient.generate", new_callable=AsyncMock)
    async def test_generate_uses_gemini(self, mock_generate):
        mock_generate.return_value = LLMResult(text="Hello", provider="gemini")
        self.manager.providers["gemini"].available = True
        result = await self.manager.generate("hello")
        self.assertTrue(mock_generate.called)
        self.assertEqual(result.provider, "gemini")

    async def test_generate_raises_when_no_provider(self):
        manager = LLMProviderManager(self.settings)
        manager.providers["gemini"].available = False
        with self.assertRaises(LLMError):
            await manager.generate("hello")


if __name__ == "__main__":
    unittest.main()
