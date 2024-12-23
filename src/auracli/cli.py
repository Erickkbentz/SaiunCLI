import logging

from typing import Optional, List, Dict, Any, Literal
from rich.console import Console

class Option:
    def __init__(
            self,
            flag: str,
            short_flag: Optional[str] = None,
            message: Optional[str] = None,
            required: Optional[bool] = False,
            action: Optional[
                Literal[
                    "store",
                    "store_true",
                    "store_false",
                    "append",
                    "extend",
                    "count",
                    "help",
                    "version"
                ]
            ] = "store",
            default: Optional[str] = None,
            prompt: Optional[bool] = False,
            prompt_message: Optional[str] = None,
            choices: Optional[List[Any]] = None,
            type: Optional[type] = str,
    ):
        self.flag = flag
        self.short_flag = short_flag
        self.message = message
        self.required = required
        self.action = action
        self.default = default
        self.prompt = prompt
        self.prompt_message = prompt_message
        self.choices = choices
        self.type = type

    def validate(self, value: Any) -> bool:
        """Validate the value of the option."""
        pass

    def parse(self, raw_value: str) -> Any:
        """Parse the raw value from the command line."""
        pass
    
    def handle(self, value: Optional[Any]) -> Any:
        """Handle the value of the option based on Option setup."""
        pass


class Command:
    def __init__(
            self,
            name: str,
            handler: callable = None,
            description: Optional[str] = None,
            options: Optional[List[Option]] = None,
            subcommands: Optional[List["Command"]] = None,
    ):
        self.name = name
        self.handler = handler
        self.description = description
        self.options = options or []
        self.subcommands = subcommands or []

    def add_option(self, option: Option):
        pass

    def add_options(self, options: List[Option]):
        pass

    def add_subcommand(self, subcommand: "Command"):
        pass

    def add_subcommands(self, subcommands: List["Command"]):
        pass

    def parse_args(self, raw_args: List[str]) -> Dict[str, Any]:
        pass

    def execute(self, args: Dict[str, Any]):
        self.handler(args)


class Theme:
    BASE_THEME_FILE = ".auracli-theme"

    def __init__(
            self,
            styles: Optional[Dict[str, str]] = None,
    ):
        self.styles = styles

    @classmethod
    def load_theme(cls, theme_file: str = BASE_THEME_FILE) -> "Theme":
        import configparser
        import os

        parser = configparser.ConfigParser()
        if not os.path.exists(theme_file):
            raise FileNotFoundError(f"Theme file '{theme_file}' not found.")

        parser.read(theme_file)

        if not parser.has_section("auracli.styles"):
            raise ValueError("Invalid theme file, missing [auracli.styles] section.")
        
        styles = {
            key: value
            for key, value in parser.items("auracli.styles")
        }
        return cls(styles=styles)


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


class AuraConsole:
    def __init__(
            self,
            theme: Optional[Theme] = None,
    ):
        self.theme = theme
        self.console = Console()
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        pass

    def log(self, message: str, level: Optional[int] = logging.INFO):
        pass

    def error(self, message: str):
        pass

    def debug(self, message: str):
        pass

    def info(self, message: str):
        pass

    def warning(self, message: str):
        pass

    def print(self, message: str):
        pass

    def print_table(self, data: List[Dict[str, Any]]):
        pass

    def print_json(self, data: Dict[str, Any]):
        pass

    def print_yaml(self, data: Dict[str, Any]):
        pass

    def progress(self, message: str):
        pass

    def spinner(self, message: str):
        pass