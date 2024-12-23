from typing import List, Optional, Dict, Any

from auracli import Option
from auracli._utils import _validate_options

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

        _validate_options(self.options)

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