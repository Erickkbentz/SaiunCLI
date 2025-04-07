from typing import Optional
from dataclasses import dataclass

from rich.style import Style

__all__ = ["Theme", "Style", "PrefixStyle"]


@dataclass
class PrefixStyle:
    symbol: str
    style: str


class Theme:

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

    DEFAULT_PREFIXES = {
        "success": PrefixStyle("✔", "bold green"),
        "error": PrefixStyle("✖", "bold red"),
        "warning": PrefixStyle("!", "bold yellow"),
        "info": PrefixStyle("ℹ", "bold blue"),
    }

    def __init__(
        self,
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
        success_prefix: Optional[PrefixStyle] = None,
        error_prefix: Optional[PrefixStyle] = None,
        warning_prefix: Optional[PrefixStyle] = None,
        info_prefix: Optional[PrefixStyle] = None,
    ):
        """
        Initialize a Theme object with custom styles and prefixes.

        Args:
            version (Optional[Style]): Style for the version text.
            title (Optional[Style]): Style for the title text.
            title_description (Optional[Style]): Style for the title description text.
            usage (Optional[Style]): Style for the usage text.
            option_long (Optional[Style]): Style for long option flags.
            option_short (Optional[Style]): Style for short option flags.
            option_description (Optional[Style]): Style for option descriptions.
            subcommand (Optional[Style]): Style for subcommand names.
            subcommand_description (Optional[Style]): Style for subcommand descriptions.
            argument (Optional[Style]): Style for argument names.
            argument_description (Optional[Style]): Style for argument descriptions.
            success_prefix (Optional[PrefixStyle]): Prefix style for success messages.
            error_prefix (Optional[PrefixStyle]): Prefix style for error messages.
            warning_prefix (Optional[PrefixStyle]): Prefix style for warning messages.
            info_prefix (Optional[PrefixStyle]): Prefix style for info messages.
        """

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
        self.success_prefix = success_prefix or self.DEFAULT_PREFIXES["success"]
        self.error_prefix = error_prefix or self.DEFAULT_PREFIXES["error"]
        self.warning_prefix = warning_prefix or self.DEFAULT_PREFIXES["warning"]
        self.info_prefix = info_prefix or self.DEFAULT_PREFIXES["info"]
