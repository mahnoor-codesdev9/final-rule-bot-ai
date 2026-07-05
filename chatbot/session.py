"""
Session management for RuleBot AI.
Compatible with Vercel (read-only filesystem).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class SessionManager:
    """Manage chat history."""

    def __init__(self, path: str | Path = "chatbot/data/chat_history.json") -> None:
        self.path = Path(path)
        self._memory_history: list[dict[str, Any]] = []

    def load(self) -> list[dict[str, Any]]:
        try:
            if self.path.exists():
                with self.path.open("r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass

        return self._memory_history

    def save(self, history: list[dict[str, Any]]) -> None:
        self._memory_history = history

        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)

            with self.path.open("w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)

        except OSError:
            # Read-only filesystem (Vercel)
            pass

    def append(
        self,
        role: str,
        message: str,
        mode: str | None = None,
        provider: str | None = None,
    ) -> None:
        """Append a single message."""

        history = self.load()

        history.append(
            {
                "role": role,
                "message": message,
                "mode": mode,
                "provider": provider,
            }
        )

        self.save(history)

    def clear(self) -> None:
        self._memory_history = []

        try:
            if self.path.exists():
                self.path.unlink()
        except Exception:
            pass