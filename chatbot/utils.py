"""
Utility functions for RuleBot AI.

This module contains reusable helper functions used
throughout the chatbot project.
"""

import re


def normalize_input(user_input: str) -> str:
    """
    Normalize user input.

    Operations:
    - Remove leading/trailing spaces
    - Convert to lowercase
    - Replace multiple spaces with one

    Args:
        user_input: Raw user input.

    Returns:
        Cleaned user input.
    """
    cleaned = user_input.strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def is_empty(user_input: str) -> bool:
    """
    Check whether the input is empty.

    Args:
        user_input: User message.

    Returns:
        True if empty, otherwise False.
    """
    return len(user_input.strip()) == 0


def contains_numbers(text: str) -> bool:
    """
    Check whether the text contains digits.

    Args:
        text: Input text.

    Returns:
        True if digits are found.
    """
    return any(character.isdigit() for character in text)


def word_count(text: str) -> int:
    """
    Count the number of words.

    Args:
        text: Input text.

    Returns:
        Total number of words.
    """
    if is_empty(text):
        return 0

    return len(text.split())


def character_count(text: str) -> int:
    """
    Count characters.

    Args:
        text: Input text.

    Returns:
        Total characters.
    """
    return len(text)


def reverse_text(text: str) -> str:
    """
    Reverse text.

    Args:
        text: Input text.

    Returns:
        Reversed text.
    """
    return text[::-1]
