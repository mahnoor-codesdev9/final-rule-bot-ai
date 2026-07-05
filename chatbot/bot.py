"""
Main chatbot engine.
"""

from chatbot.commands import CommandHandler
from chatbot.config import (
    BOT_NAME,
    EXIT_COMMANDS,
    GOODBYE_MESSAGE,
    UNKNOWN_RESPONSE,
    WELCOME_MESSAGE,
)
from chatbot.formatter import (
    clear_screen,
    print_banner,
    print_bot,
)
from chatbot.history import ChatHistory
from chatbot.logger import ChatLogger
from chatbot.matcher import ResponseMatcher
from chatbot.session import ChatSession
from chatbot.statistics import ChatStatistics
from chatbot.utils import (
    is_empty,
    normalize_input,
)


class ChatBot:
    """
    RuleBot AI.
    """

    def __init__(self) -> None:

        self.name = BOT_NAME

        self.running = True

        self.logger = ChatLogger()

        self.history = ChatHistory()

        self.matcher = ResponseMatcher()

        self.commands = CommandHandler()

        self.session = ChatSession()

        self.statistics = ChatStatistics()

    def get_response(self, user_input: str) -> str:

        if self.commands.is_command(user_input):

            self.session.add_command()

            self.statistics.increment_commands()

            return self.commands.execute(user_input, self)

        response = self.matcher.find_response(user_input)

        if response:

            return response

        return UNKNOWN_RESPONSE

    def start(self) -> None:

        clear_screen()

        print_banner()

        print_bot(WELCOME_MESSAGE)

        self.logger.start_session()

        while self.running:

            try:

                user_input = input("ðŸ‘¤ You: ")

                user_input = normalize_input(user_input)

                if is_empty(user_input):

                    continue

                self.session.add_message()

                self.statistics.increment_messages()

                self.history.add_message("User", user_input)

                self.logger.log("User", user_input)

                if user_input in EXIT_COMMANDS:

                    print_bot(GOODBYE_MESSAGE)

                    self.logger.log("Bot", GOODBYE_MESSAGE)

                    self.logger.end_session()

                    break

                response = self.get_response(user_input)

                self.history.add_message("Bot", response)

                self.logger.log("Bot", response)

                print_bot(response)

            except KeyboardInterrupt:

                print()

                print_bot("Session interrupted.")

                self.logger.end_session()

                break

            except Exception as error:

                print_bot(f"Unexpected Error: {error}")

                self.logger.end_session()

                break
