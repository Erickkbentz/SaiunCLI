from typing import Optional, List

from auracli import AuraConsole, Theme,  Command, Option
from auracli.command import Command, _ROOT_COMMAND_NAME

class AuraCLI(Command):
    def __init__(
            self,
            title: str,
            version: Optional[str] = None,
            theme: Optional[Theme] = None,
            console: Optional[AuraConsole] = None,
            handler: callable = None,
            usage: Optional[str] = None,
            description: Optional[str] = None,
            options: Optional[List[Option]] = None,
            subcommands: Optional[List[Command]] = None,
    ):
        """
        Initialize an AuraCLI object.

        Args:
            title (str):
                The title of the CLI tool.
            version (Optional[str]):
                The version of the CLI tool.
            theme (Optional[Theme]):
                The theme to use for the CLI tool.
            console (Optional[AuraConsole]):
                The console to use for the CLI tool.
            handler (callable):
                The function to execute when the base CLI command is called.
            usage (Optional[str]):
                The usage message for the base CLI command.
            description (Optional[str]):
                The description of the base CLI command.
            options (Optional[List[Option]]):
                The options available for the base CLI command.
            subcommands (Optional[List[Command]]):
                The subcommands available for the base CLI command.
        """
        super().__init__(
            name=_ROOT_COMMAND_NAME,
            handler=handler,
            usage=usage,
            description=description,
            options=options,
            inherit_options=False,
            subcommands=subcommands,
        )

        self.title = title
        self.version = version
        self.theme = theme
        self.console = console or AuraConsole(theme=self.theme)

    def display_version(self):
        pass

    def display_cli_help(self):
        pass

    def display_command_help(self, command: Command):
        pass

    def run(self, args: Optional[List[str]] = None):
        pass