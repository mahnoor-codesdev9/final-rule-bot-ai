"""
Custom exceptions for RuleBot AI.

This module defines application-specific exception classes.
"""


class RuleBotError(Exception):
    """
    Base exception for all RuleBot AI errors.
    """

    def __init__(
        self,
        message: str = ("An unknown RuleBot error occurred."),
    ) -> None:
        super().__init__(message)


class InvalidCommandError(RuleBotError):
    """
    Raised when an invalid command is executed.
    """

    def __init__(self, command: str) -> None:
        super().__init__(f"Invalid command: '{command}'")


class ResponseNotFoundError(RuleBotError):
    """
    Raised when no suitable response is found.
    """

    def __init__(self) -> None:
        super().__init__("No matching response found.")


class LoggerError(RuleBotError):
    """
    Raised when the logger encounters an error.
    """

    def __init__(self) -> None:
        super().__init__("Logger operation failed.")


class HistoryError(RuleBotError):
    """
    Raised when conversation history operations fail.
    """

    def __init__(self) -> None:
        super().__init__("Conversation history error.")
