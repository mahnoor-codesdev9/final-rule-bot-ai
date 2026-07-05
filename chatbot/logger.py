"""
Logging module for RuleBot AI.

This module provides a reusable logger for recording
chatbot activity, user interactions, and errors.
"""

from datetime import datetime
from pathlib import Path

from chatbot.config import LOG_DIRECTORY, LOG_FILE


class ChatLogger:
    """
    Handles chatbot logging operations.
    """

    def __init__(self) -> None:
        """
        Initialize the logger.
        """
        self.log_directory = Path(LOG_DIRECTORY)
        self.log_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.log_path = self.log_directory / LOG_FILE

    def _write(self, message: str) -> None:
        """
        Write a line to the log file.
        """
        with open(
            self.log_path,
            "a",
            encoding="utf-8",
        ) as file:
            file.write(message + "\n")

    def start_session(self) -> None:
        """
        Record the beginning of a chat session.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self._write("=" * 70)

        self._write(f"SESSION STARTED : {timestamp}")

        self._write("=" * 70)

    def end_session(self) -> None:
        """
        Record the end of a chat session.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self._write("=" * 70)

        self._write(f"SESSION ENDED   : {timestamp}")

        self._write("=" * 70)

        self._write("")

    def log(
        self,
        sender: str,
        message: str,
    ) -> None:
        """
        Log a conversation message.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")

        self._write(f"[{timestamp}] " f"{sender:<5} : " f"{message}")

    def info(self, message: str) -> None:
        """
        Log an informational message.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")

        self._write(f"[{timestamp}] INFO : {message}")

    def warning(self, message: str) -> None:
        """
        Log a warning message.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")

        self._write(f"[{timestamp}] WARNING : {message}")

    def error(self, message: str) -> None:
        """
        Log an error message.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")

        self._write(f"[{timestamp}] ERROR : {message}")
