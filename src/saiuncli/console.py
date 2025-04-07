from typing import Optional, Any, List
from rich.console import Console as RichConsole
from rich.theme import Theme as RichTheme
from rich.highlighter import RegexHighlighter
from rich.text import Text
from rich.panel import Panel
from rich.table import Table

from saiuncli.theme import Theme
from saiuncli.command import Command
from saiuncli.option import Option
from saiuncli.argument import Argument


class Console:
    def __init__(self, theme: Optional["Theme"] = None):
        self.theme = theme or Theme()

        class OptionHighlighter(RegexHighlighter):
            highlights = [r"(?P<short_flag>\-\w)", r"(?P<long_flag>\-\-[\w\-]+)"]

        self._highlighter = OptionHighlighter()
        self._console = RichConsole(
            theme=RichTheme(
                {
                    "long_flag": self.theme.option_long,
                    "short_flag": self.theme.option_short,
                }
            ),
            highlighter=self._highlighter,
        )

    def print(self, *objects: Any, style: Optional[str] = None, **kwargs: Any) -> None:
        """
        Print a message to the console with the current theme.

        Args:
            msg (str): The message to print.
            **kwargs: Additional keyword arguments for RichConsole.print().
        """
        self._console.print(*objects, style=style, **kwargs)

    def success(self, message: str):
        style = self.theme.success_prefix.style
        symbol = self.theme.success_prefix.symbol
        self.print(
            f"[{style}]{symbol}[/{style}] {message}",
        )

    def error(self, message: str):
        style = self.theme.error_prefix.style
        symbol = self.theme.error_prefix.symbol
        self.print(
            f"[{style}]{symbol}[/{style}] {message}",
        )

    def warning(self, message: str):
        style = self.theme.warning_prefix.style
        symbol = self.theme.warning_prefix.symbol
        self.print(
            f"[{style}]{symbol}[/{style}] {message}",
        )

    def info(self, message: str):
        style = self.theme.info_prefix.style
        symbol = self.theme.info_prefix.symbol
        self.print(
            f"[{style}]{symbol}[/{style}] {message}",
        )

    def display_header(
        self,
        title: str,
        description: Optional[str] = None,
        version: Optional[str] = None,
    ):
        """Display the CLI tool Header Information."""
        title = Text(title, style=self.theme.title)
        if version:
            version = Text(f"v{version}", style=self.theme.version)
            title.pad_right(1)
            title.append(version)
        self.print(
            title,
            justify="center",
        )
        self.print()
        if description:
            title_description = Text(description, style=self.theme.title_description)
            self.print(
                title_description,
                justify="center",
            )
            self.print()
        self.print()

    def display_usage(self, usage: str = None):
        self.print(Text(f"Usage: {usage}"), style=self.theme.usage)

    def display_version(self, version: str):
        self.print(
            Text(
                f"v{version}",
                style=self.theme.version,
            ),
            justify="left",
        )

    def display_subcommands_table(self, subcommands: Optional[List[Command]] = None):
        if not subcommands:
            return
        subcommands_table = Table(highlight=True, box=None, show_header=False)
        for subcommand in subcommands:
            help_message = (
                Text.from_markup(subcommand.description) if subcommand.description else Text("")
            )
            help_message.style = self.theme.subcommand_description

            if subcommand.description:
                subcommand_name = Text(subcommand.name, style=self.theme.subcommand)
                subcommand_name.pad_right(5)

                subcommands_table.add_row(subcommand_name, help_message)
        self.print(
            Panel(subcommands_table, border_style="dim", title_align="left", title="Subcommands")
        )

    def display_options_table(
        self,
        options: Optional[List[Option]],
        version_flags: Optional[List[str]] = None,
        help_flags: Optional[List[str]] = None,
    ):
        """Display the options table for the CLI tool.

        Args:
            command (Optional[Command]):
                The command to display options for.
        """
        if not options:
            return

        options_table = Table(highlight=True, box=None, show_header=False)
        for option in options:
            help_message = Text("")
            if option.description:
                help_message = Text.from_markup(option.description)
                help_message.style = self.theme.option_description
            if len(option.flags) == 2:
                opt1 = self._highlighter(option.flags[0])
                opt2 = self._highlighter(option.flags[1])
            else:
                opt1 = self._highlighter(option.flags[0])
                opt2 = Text("")
            opt2.pad_right(5)
            options_table.add_row(opt1, opt2, help_message)
        # Always add version flags to the bottom of Global Options table
        if len(version_flags) == 2:
            version_flag1 = self._highlighter(version_flags[0])
            version_flag2 = self._highlighter(version_flags[1])
        else:
            version_flag1 = self._highlighter(version_flags[0])
            version_flag2 = Text("")
        version_flag2.pad_right(5)
        options_table.add_row(
            version_flag1,
            version_flag2,
            Text("Display the version.", style=self.theme.option_description),
        )
        # Always add help flags to the bottom Global Options table
        if len(help_flags) == 2:
            help_flag1 = self._highlighter(help_flags[0])
            help_flag2 = self._highlighter(help_flags[1])
        else:
            help_flag1 = self._highlighter(help_flags[0])
            help_flag2 = Text("")
        help_flag2.pad_right(5)
        options_table.add_row(
            help_flag1,
            help_flag2,
            Text("Display this help message and exit.", style=self.theme.option_description),
        )
        self.print(Panel(options_table, border_style="dim", title_align="left", title="Options"))

    def display_arguments_table(
        self,
        arguments: Optional[List[Argument]] = None,
    ):
        if not arguments:
            return

        arguments_table = Table(highlight=True, box=None, show_header=False)
        for argument in arguments:
            help_message = ""
            if argument.description:
                help_message = Text.from_markup(argument.description)
                help_message.style = self.theme.argument_description

                argument_name = Text(argument.name, style=self.theme.argument)
                arguments_table.add_row(argument_name, help_message)
        self.print(
            Panel(arguments_table, border_style="dim", title_align="left", title="Arguments")
        )

    def display_help(
        self,
        title: str = None,
        usage: str = None,
        description: Optional[str] = None,
        version: Optional[str] = None,
        options: Optional[str] = None,
        arguments: Optional[str] = None,
        subcommands: Optional[str] = None,
        show_header: bool = True,
        help_flags: Optional[List[str]] = None,
        version_flags: Optional[List[str]] = None,
    ):
        if show_header and title:
            self.display_header(title, description, version)

        self.display_usage(usage)
        self.display_subcommands_table(subcommands=subcommands)
        self.display_options_table(
            options=options, version_flags=version_flags, help_flags=help_flags
        )
        self.display_arguments_table(arguments=arguments)
