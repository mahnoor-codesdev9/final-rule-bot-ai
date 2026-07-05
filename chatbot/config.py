"""
Configuration constants for the terminal chatbot.

The FastAPI application reads deployment settings from `core.settings`.
These constants remain stable for the CLI bot and existing imports.
"""

APP_NAME: str = "RuleBot AI"
VERSION: str = "2.1.0"
AUTHOR: str = "RuleBot AI"
DESCRIPTION: str = (
    "A production-ready rule-based AI assistant "
    "built with Python."
)

BOT_NAME: str = "RuleBot"
BOT_PROMPT: str = "RuleBot"
USER_PROMPT: str = "You"

WELCOME_MESSAGE: str = (
    "Hello! Welcome to RuleBot AI.\n" "Type 'help' to see available commands."
)
GOODBYE_MESSAGE: str = "Goodbye! Thanks for using RuleBot AI."
UNKNOWN_RESPONSE: str = (
    "I don't have a specific answer for that yet, but I'm happy to help if "
    "you rephrase it, ask about a related topic, or give me a bit more detail."
)

EXIT_COMMANDS: tuple[str, ...] = (
    "exit",
    "quit",
    "bye",
)

LOG_DIRECTORY: str = "chatbot/logs"
LOG_FILE: str = "chat.log"

LINE_WIDTH: int = 70
TYPING_SPEED: float = 0.02
