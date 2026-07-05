"""
Command system for RuleBot AI.

This module manages all built-in chatbot commands.
"""

from chatbot.formatter import clear_screen, print_banner


class CommandHandler:
    """
    Handles chatbot commands.
    """

    def __init__(self) -> None:
        """
        Register all available commands.
        """
        self._commands = {
            "help": self.help_command,
            "history": self.history_command,
            "clear": self.clear_command,
            "about": self.about_command,
        }

    def is_command(self, user_input: str) -> bool:
        """
        Check whether the input is a valid command.
        """
        return user_input in self._commands

    def execute(self, command: str, chatbot) -> str:
        """
        Execute a command.

        Args:
            command: Command entered by the user.
            chatbot: ChatBot instance.

        Returns:
            Command output.
        """
        return self._commands[command](chatbot)

    def help_command(self, chatbot) -> str:
        """
        Display all available commands.
        """
        return (
            "Available Commands\n"
            "------------------\n"
            "help     - Show available commands\n"
            "history  - Show conversation history\n"
            "clear    - Clear the terminal screen\n"
            "about    - About RuleBot AI\n"
            "exit     - Exit the application"
        )

    def history_command(self, chatbot) -> str:
        """
        Display conversation history.
        """
        return chatbot.history.formatted_history()

    def clear_command(self, chatbot) -> str:
        """
        Clear the terminal.
        """
        clear_screen()
        print_banner()
        return "Screen cleared."

    def about_command(self, chatbot) -> str:
        """
        Display application information.
        """
        return (
            "RuleBot AI\n"
            "Version: 1.0.0\n"
            "Language: Python\n"
            "Architecture: Object-Oriented & Modular\n"
            "Purpose: Professional Rule-Based AI Chatbot"
        )

    def available_commands(self) -> list[str]:
        """
        Return all registered commands.
        """
        return sorted(self._commands.keys())
