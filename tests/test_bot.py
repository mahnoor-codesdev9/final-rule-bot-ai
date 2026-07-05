"""
Unit tests for RuleBot AI.
"""

import unittest

from chatbot.bot import ChatBot
from chatbot.config import UNKNOWN_RESPONSE
from chatbot.matcher import ResponseMatcher
from chatbot.utils import (
    is_empty,
    normalize_input,
    word_count,
)


class TestUtils(unittest.TestCase):
    """Tests for utility functions."""

    def test_normalize_input(self):
        self.assertEqual(
            normalize_input("   HELLO   "),
            "hello",
        )

    def test_empty_input(self):
        self.assertTrue(is_empty(""))

    def test_word_count(self):
        self.assertEqual(
            word_count("Python is awesome"),
            3,
        )


class TestMatcher(unittest.TestCase):
    """Tests for response matcher."""

    def setUp(self):
        self.matcher = ResponseMatcher()

    def test_known_response(self):
        response = self.matcher.find_response("hello")
        self.assertIsNotNone(response)

    def test_unknown_response(self):
        response = self.matcher.find_response("abcdefgh")
        self.assertEqual(
            response,
            UNKNOWN_RESPONSE,
        )


class TestChatBot(unittest.TestCase):
    """Tests for chatbot."""

    def setUp(self):
        self.bot = ChatBot()

    def test_bot_created(self):
        self.assertEqual(
            self.bot.name,
            "RuleBot",
        )

    def test_message_counter(self):
        self.assertEqual(
            self.bot.session.message_count,
            0,
        )

    def test_command_counter(self):
        self.assertEqual(
            self.bot.session.command_count,
            0,
        )


if __name__ == "__main__":
    unittest.main()
