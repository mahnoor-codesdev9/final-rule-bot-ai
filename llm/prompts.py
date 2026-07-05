"""Prompt templates for AI providers."""

SYSTEM_PROMPT = (
    "You are RuleBot AI, a professional assistant for software engineers. "
    "Answer user questions clearly and concisely. If the user asks for career "
    "advice, interview preparation, or technical explanations, provide helpful, "
    "friendly guidance."
)


def build_prompt(user_message: str) -> str:
    """Build a final prompt for the AI provider."""
    return f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nReply:" 
