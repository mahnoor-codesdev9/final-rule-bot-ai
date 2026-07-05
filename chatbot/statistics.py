"""
Runtime statistics for RuleBot AI.
"""

from __future__ import annotations

from datetime import datetime


class Statistics:
    """
    Track web chat message counts for the active server process.
    """

    def __init__(self) -> None:
        self.reset()

    def user_message(self) -> None:
        """
        Count one user message.
        """
        self.user_messages += 1

    def bot_message(
        self,
        mode: str = "rule",
        fallback: bool = False,
    ) -> None:
        """
        Count one bot response and its response type.
        """
        self.bot_messages += 1

        if mode == "ai" and not fallback:
            self.ai_responses += 1
        else:
            self.rule_responses += 1

        if fallback:
            self.fallbacks += 1

    def reset(self) -> None:
        """
        Reset counters and session duration.
        """
        self.started = datetime.now()
        self.user_messages = 0
        self.bot_messages = 0
        self.rule_responses = 0
        self.ai_responses = 0
        self.fallbacks = 0

    def to_dict(self) -> dict[str, int]:
        """
        Return serializable statistics for the API.
        """
        duration = datetime.now() - self.started

        return {
            "user_messages": self.user_messages,
            "bot_messages": self.bot_messages,
            "total_messages": self.user_messages + self.bot_messages,
            "session_seconds": int(duration.total_seconds()),
            "rule_responses": self.rule_responses,
            "ai_responses": self.ai_responses,
            "fallbacks": self.fallbacks,
        }


class ChatStatistics:
    """
    Track terminal chatbot message and command counts.
    """

    def __init__(self) -> None:
        self.message_count = 0
        self.command_count = 0

    def increment_messages(self) -> None:
        """
        Count one terminal message.
        """
        self.message_count += 1

    def increment_commands(self) -> None:
        """
        Count one terminal command.
        """
        self.command_count += 1

    def reset(self) -> None:
        """
        Reset terminal statistics.
        """
        self.message_count = 0
        self.command_count = 0
