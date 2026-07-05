"""
Conversation history manager for RuleBot AI.

This module manages the complete conversation history
between the user and the chatbot.
"""

from datetime import datetime


class ChatHistory:
    """
    Manages chatbot conversation history.
    """

    def __init__(self) -> None:
        """
        Initialize an empty conversation history.
        """
        self._messages: list[dict[str, str]] = []

    def add_message(
        self,
        sender: str,
        message: str,
    ) -> None:
        """
        Add a message to the conversation history.
        """

        self._messages.append(
            {
                "time": datetime.now().strftime("%H:%M:%S"),
                "sender": sender,
                "message": message,
            }
        )

    def clear(self) -> None:
        """
        Remove all conversation history.
        """
        self._messages.clear()

    def total_messages(self) -> int:
        """
        Return total number of stored messages.
        """
        return len(self._messages)

    def is_empty(self) -> bool:
        """
        Check whether the conversation history is empty.
        """
        return len(self._messages) == 0

    def last_message(
        self,
    ) -> dict[str, str] | None:
        """
        Return the most recent message.
        """
        if self.is_empty():
            return None

        return self._messages[-1]

    def get_messages(
        self,
    ) -> list[dict[str, str]]:
        """
        Return all stored messages.
        """
        return self._messages.copy()

    def formatted_history(self) -> str:
        """
        Return conversation history as formatted text.
        """
        if self.is_empty():
            return "No conversation history available."

        lines: list[str] = []

        for item in self._messages:
            lines.append(
                f"[{item['time']}] " f"{item['sender']}: " f"{item['message']}"
            )

        return "\n".join(lines)
