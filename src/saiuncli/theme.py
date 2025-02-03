from typing import Dict, Optional
from rich.style import Style


class Theme:
    BASE_THEME_FILE = ".auracli-theme"

    DEFAULT_STYLES = {
        "version": Style(color="magenta", bold=True, italic=True),
        "title": Style(color="white", bold=True),
        "title_description": Style(color="white", dim=True),
        "usage": Style(color="white", bold=True),
        "option_long": Style(color="cyan", bold=True),
        "option_short": Style(color="green", bold=True),
        "option_description": Style(color="white"),
        "subcommand": Style(color="cyan", bold=True),
        "subcommand_description": Style(color="white"),
        "argument": Style(color="cyan", bold=True),
        "argument_description": Style(color="white"),
    }

    def __init__(
        self,
        styles: Optional[Dict[str, Style]] = None,
        version: Optional[Style] = None,
        title: Optional[Style] = None,
        title_description: Optional[Style] = None,
        usage: Optional[Style] = None,
        option_long: Optional[Style] = None,
        option_short: Optional[Style] = None,
        option_description: Optional[Style] = None,
        subcommand: Optional[Style] = None,
        subcommand_description: Optional[Style] = None,
        argument: Optional[Style] = None,
        argument_description: Optional[Style] = None,
    ):
        self.styles = styles or {}

        self.version = version or self.DEFAULT_STYLES["version"]
        self.title = title or self.DEFAULT_STYLES["title"]
        self.title_description = title_description or self.DEFAULT_STYLES["title_description"]
        self.usage = usage or self.DEFAULT_STYLES["usage"]
        self.option_long = option_long or self.DEFAULT_STYLES["option_long"]
        self.option_short = option_short or self.DEFAULT_STYLES["option_short"]
        self.option_description = option_description or self.DEFAULT_STYLES["option_description"]
        self.subcommand = subcommand or self.DEFAULT_STYLES["subcommand"]
        self.subcommand_description = (
            subcommand_description or self.DEFAULT_STYLES["subcommand_description"]
        )
        self.argument = argument or self.DEFAULT_STYLES["argument"]
        self.argument_description = (
            argument_description or self.DEFAULT_STYLES["argument_description"]
        )

        for key in self.DEFAULT_STYLES:
            if key not in self.styles:
                self.styles[key] = getattr(self, key)

    @classmethod
    def load_theme(cls, theme_file: str = BASE_THEME_FILE) -> "Theme":
        """_summary_

        Args:
            theme_file (str, optional): _description_. Defaults to BASE_THEME_FILE.

        Returns:
            Theme: _description_
        """
        pass
