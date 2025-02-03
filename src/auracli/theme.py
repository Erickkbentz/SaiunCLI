from typing import Dict, Optional
from rich.style import Style


class Theme:
    BASE_THEME_FILE = ".auracli-theme"

    def __init__(
        self,
        styles: Optional[Dict[str, Style]] = None,
        version: Optional[Style] = None,
        title: Optional[Style] = None,
        title_description: Optional[Style] = None,
        usage: Optional[Style] = None,
        option: Optional[Style] = None,
        option_description: Optional[Style] = None,
        subcommand: Optional[Style] = None,
        subcommand_description: Optional[Style] = None,
        argument: Optional[Style] = None,
        argument_description: Optional[Style] = None,
    ):
        self.styles = styles or {}
        self.version = version or Style(color="magenta", bold=True, italic=True)
        self.title = title or Style(color="white", bold=True)
        self.title_description = title_description or Style(color="white", dim=True)
        self.usage = usage or Style(color="white", bold=True)
        self.option_short = option or Style(color="green", bold=True)
        self.option_long = option or Style(color="cyan", bold=True)
        self.option_description = option_description or Style(color="white")
        self.subcommand = subcommand or Style(color="cyan", bold=True)
        self.subcommand_description = subcommand_description or Style(color="white")
        self.argument = argument or Style(color="cyan", bold=True)
        self.argument_description = argument_description or Style(color="white")

        if not self.styles:
            self.styles = {
                "version": self.version,
                "title": self.title,
                "title_description": self.title_description,
                "usage": self.usage,
                "option_short": self.option_short,
                "option_long": self.option_long,
                "option_description": self.option_description,
                "subcommand": self.subcommand,
                "subcommand_description": self.subcommand_description,
                "argument": self.argument,
                "argument_description": self.argument_description,
            }

    @classmethod
    def load_theme(cls, theme_file: str = BASE_THEME_FILE) -> "Theme":
        """_summary_

        Args:
            theme_file (str, optional): _description_. Defaults to BASE_THEME_FILE.

        Returns:
            Theme: _description_
        """
        pass
