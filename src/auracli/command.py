from typing import List, Optional, Dict, Any

from auracli import Option
from auracli._utils import _validate_options

_ROOT_COMMAND_NAME = "root"

class Command:
    _parent: "Command" = None

    def __init__(
            self,
            name: str,
            handler: callable = None,
            usage: Optional[str] = None,
            description: Optional[str] = None,
            options: Optional[List[Option]] = None,
            inherit_options: Optional[bool] = False,
            subcommands: Optional[List["Command"]] = None,
    ):
        self.name = name
        self.handler = handler
        self.usage = usage
        self.description = description
        self.inherit_options = inherit_options
        self.options = options or []
        self.subcommands = subcommands or []

        for subcommand in self.subcommands:
            subcommand._parent = self

        _validate_options(self.all_options)

    @property
    def inherited_options(self) -> List[Option]:
        """
        Gather options inherited from parent commands if inheritance is enabled.
        """
        if not self.inherit_options:
            return []
        inherited = []
        parent = self._parent
        while parent:
            inherited.extend(parent.options)
            parent = parent._parent
        return inherited

    @property
    def all_options(self) -> List[Option]:
        return self.inherited_options + self.options


    def add_option(self, option: Option):
        """Add an option to the command."""
        self.options.append(option)
        _validate_options(self.all_options)
        pass

    def add_options(self, options: List[Option]):
        """Add multiple options to the command."""
        self.options.extend(options)
        _validate_options(self.all_options)
        pass

    def add_subcommand(self, subcommand: "Command"):
        """Add a subcommand to the command."""
        subcommand._parent = self
        self.subcommands.append(subcommand)
        pass

    def add_subcommands(self, subcommands: List["Command"]):
        """Add multiple subcommands to the command."""
        for subcommand in subcommands:
            subcommand._parent = self
        self.subcommands.extend(subcommands)
        pass

    def parse_args(self, raw_args: List[str]) -> Dict[str, Any]:
        pass

    def execute(self, args: Dict[str, Any]):
        self.handler(args)