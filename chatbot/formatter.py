"""
Terminal formatting utilities for RuleBot AI.

This module is responsible for displaying
formatted output in the terminal.
"""

import os
import time

from colorama import Fore, Style, init

from chatbot.config import (
    APP_NAME,
    BOT_PROMPT,
    LINE_WIDTH,
    TYPING_SPEED,
    USER_PROMPT,
    VERSION,
)

# Initialize Colorama
init(autoreset=True)


def clear_screen() -> None:
    """
    Clear the terminal screen.
    """
    os.system("cls" if os.name == "nt" else "clear")


def divider() -> None:
    """
    Print a horizontal divider.
    """
    print(Fore.CYAN + "=" * LINE_WIDTH)


def print_banner() -> None:
    """
    Display the application banner.
    """
    divider()
    print(Fore.CYAN + Style.BRIGHT + f"{APP_NAME:^{LINE_WIDTH}}")
    print(Fore.CYAN + f"Version {VERSION}")
    divider()
    print()


def typing_effect(message: str) -> None:
    """
    Print text with a typing animation.

    Args:
        message: Text to display.
    """
    for character in message:
        print(character, end="", flush=True)
        time.sleep(TYPING_SPEED)

    print()


def print_bot(message: str) -> None:
    """
    Display a bot message.

    Args:
        message: Bot response.
    """
    print(Fore.GREEN + f"{BOT_PROMPT}: ", end="")
    typing_effect(message)


def print_user(message: str) -> None:
    """
    Display a user message.

    Args:
        message: User input.
    """
    print(Fore.CYAN + f"{USER_PROMPT}: {message}")


def print_success(message: str) -> None:
    """
    Display a success message.
    """
    print(Fore.GREEN + f"[SUCCESS] {message}")


def print_info(message: str) -> None:
    """
    Display an informational message.
    """
    print(Fore.YELLOW + f"[INFO] {message}")


def print_warning(message: str) -> None:
    """
    Display a warning message.
    """
    print(Fore.LIGHTYELLOW_EX + f"[WARNING] {message}")


def print_error(message: str) -> None:
    """
    Display an error message.
    """
    print(Fore.RED + Style.BRIGHT + f"[ERROR] {message}")
