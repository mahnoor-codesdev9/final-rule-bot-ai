"""
Session management for RuleBot AI.

The web app stores persistent chat history on disk, while the terminal chatbot
keeps lightweight in-memory counters for tests and CLI analytics.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class SessionManager:
    """
    Manage persistent web chat history.
    """

    def __init__(
        self,
        path: str | Path = "chatbot/data/chat_history.json",
    ) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.path.exists():
            self.save([])

    def load(self) -> list[dict[str, Any]]:
        """
        Load saved chat messages and normalize legacy records.
        """
        try:
            with self.path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return []

        if not isinstance(data, list):
            return []

        normalized: list[dict[str, Any]] = []

        for item in data:
            if not isinstance(item, dict):
                continue

            sender = str(item.get("sender", "")).strip()
            message = str(item.get("message", "")).strip()

            if not sender or not message:
                continue

            normalized.append(
                {
                    "sender": sender,
                    "message": message,
                    "mode": item.get("mode", "rule"),
                    "provider": item.get("provider"),
                    "timestamp": item.get("timestamp"),
                }
            )

        return normalized

    def save(
        self,
        history: list[dict[str, Any]],
    ) -> None:
        """
        Persist chat messages in a stable JSON format.
        """
        with self.path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                history,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def append(
        self,
        sender: str,
        message: str,
        mode: str = "rule",
        provider: str | None = None,
    ) -> None:
        """
        Append one message to the persistent history.
        """
        history = self.load()
        history.append(
            {
                "sender": sender,
                "message": message,
                "mode": mode,
                "provider": provider,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
        self.save(history)

    def clear(self) -> None:
        """
        Clear persistent chat history.
        """
        self.save([])


class ChatSession:
    """
    Track terminal chatbot session counters.
    """

    def __init__(self) -> None:
        self.message_count = 0
        self.command_count = 0

    def add_message(self) -> None:
        """
        Count one user message.
        """
        self.message_count += 1

    def add_command(self) -> None:
        """
        Count one command execution.
        """
        self.command_count += 1

    def reset(self) -> None:
        """
        Reset terminal session counters.
        """
        self.message_count = 0
        self.command_count = 0
