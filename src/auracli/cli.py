from typing import Optional, List
from auracli.command import Command
from auracli.theme import Theme

class AuraCLI:
    def __init__(
            self,
            title: str,
            commands: List[Command],
            description: Optional[str] = None,
            version: Optional[str] = None,
            theme: Optional[Theme] = None,
    ):
        if not commands or len(commands) == 0:
            raise ValueError("At least one command must be provided.")

        self.title = title
        self.commands = commands

        self.description = description
        self.version = version
        self.theme = theme

    def display_help():
        pass

    def run(self, args: Optional[List[str]] = None):
        import sys
        args = args or sys.argv[1:]