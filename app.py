"""
RuleBot AI

Application entry point.
"""

from chatbot.bot import ChatBot


def main() -> None:
    """
    Create and start the chatbot.
    """

    chatbot = ChatBot()

    chatbot.start()


if __name__ == "__main__":
    main()
