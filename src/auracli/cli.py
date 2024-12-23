from typing import Optional, List

from auracli import AuraConsole, Theme,  Command, Option
from auracli._utils import _validate_options, _is_flag

class AuraCLI():
    def __init__(
            self,
            title: str,
            base_handler: Optional[callable] = None,
            description: Optional[str] = None,
            version: Optional[str] = None,
            usage: Optional[str] = None,
            theme: Optional[Theme] = None,
            console: Optional[AuraConsole] = None,
            commands: Optional[List[Command]] = None,
            options: Optional[List[Option]] = None,
    ):

        self.title = title
        self.base_handler = base_handler
        self.description = description
        self.version = version
        self.usage = usage
        self.theme = theme
        self.console = console or AuraConsole(theme=self.theme)
        self.commands = {command.name: command for command in commands or []}
        self.options = options or []

        _validate_options(self.options)

    def display_cli_help(self):
        pass

    def display_command_help(self, command: Command):
        pass

    def run(self, args: Optional[List[str]] = None):
        import sys
        args = args or sys.argv[1:]

        if _is_flag(args[0]):
            self.base_handler(args)
            return
        if args[0] in self.commands:
            command = self.commands[args[0]]
            command.execute(command.parse_args(args[1:]))
            return