from typing import List, Optional, Dict, Any

from auracli.option import Option
from auracli.argument import Argument

_ROOT_COMMAND_NAME = "root"


class Command:
    _parent: "Command" = None

    def __init__(
        self,
        name: str,
        handler: callable,
        usage: Optional[str] = None,
        description: Optional[str] = None,
        options: Optional[List[Option]] = None,
        inherit_options: Optional[bool] = False,
        arguments: Optional[Argument] = None,
        inherit_arguments: Optional[bool] = False,
        subcommands: Optional[List["Command"]] = None,
    ):
        """
        Initialize a Command object.

        Args:
            name (str):
                The name of the command.
            handler (callable):
                The function to execute when the command is called.
            usage (Optional[str]):
                The usage message for the command.
            description (Optional[str]):
                The description of the command.
            options (Optional[List[Option]]):
                The options available for the command.
            inherit_options (Optional[bool]):
                Whether to inherit options from parent commands.
            arguments (Optional[Argument]):
                The arguments available for the command.
            inherit_arguments (Optional[bool]):
                Whether to inherit arguments from parent commands.
            subcommands (Optional[List[Command]]):
                The subcommands available for the command.
        """
        self.name = name
        self.handler = handler
        self.usage = usage
        self.description = description
        self.options = options or []
        self.inherit_options = inherit_options
        self.arguments = arguments or []
        self.inherit_arguments = inherit_arguments
        self.subcommands = subcommands or []

        for subcommand in self.subcommands:
            subcommand._parent = self

        self._validate_options(self.all_options)

    def _validate_options(self, options: List[Option]):
        """
        Ensure there are no duplicate flags across all options.
        """
        flag_set = set()
        for option in options:
            for flag in option.flags:
                if flag in flag_set:
                    raise ValueError(
                        f"Duplicate flag detected: {flag}. Flags must be unique between commands."
                    )
                flag_set.add(flag)

    def _validate_arguments(self, arguments: List[Argument]):
        """
        Ensure there are no duplicate names across all arguments.
        """
        name_set = set()
        for argument in arguments:
            if argument.name in name_set:
                raise ValueError(
                    f"Duplicate argument detected: {argument.name}. "
                    + "Arguments must be unique between commands."
                )
            name_set.add(argument.name)

    @property
    def inherited_arguments(self) -> List[Argument]:
        """
        Gather arguments inherited from parent commands if inheritance is enabled.
        """
        if not self.inherit_arguments:
            return []
        inherited = []
        parent = self._parent
        while parent:
            inherited.extend(parent.arguments)
            parent = parent._parent
        return inherited

    @property
    def all_arguments(self) -> List[Argument]:
        """
        Gather all arguments available to the command.
        """
        return self.inherited_arguments + self.arguments

    @property
    def all_argument_names(self) -> List[str]:
        """
        Gather all argument names available to the command.
        """
        argument_names = []
        for argument in self.all_arguments:
            argument_names.append(argument.name)
        return argument_names

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
        """
        Gather all options available to the command.
        """
        return self.inherited_options + self.options

    @property
    def all_option_names(self) -> List[Option]:
        """
        Gather all options available to the command.
        """
        option_names = []
        for option in self.all_options:
            option_names.extend(option.name)
        return option_names

    @property
    def all_comands(self) -> List["Command"]:
        """
        Gather all commands available to the command.
        """
        commands = [self]
        for subcommand in self.subcommands:
            commands.extend(subcommand.all_commands)
        return commands

    @property
    def all_command_names(self) -> List[str]:
        """
        Gather all command names available to the command.
        """
        command_names = [self.name]
        for subcommand in self.subcommands:
            command_names.extend(subcommand.all_command_names)
        return command_names

    def add_option(self, option: Option):
        """Add an option to the command."""
        self.options.append(option)
        self._validate_options(self.all_options)

    def add_options(self, options: List[Option]):
        """Add multiple options to the command."""
        self.options.extend(options)
        self._validate_options(self.all_options)

    def add_subcommand(self, subcommand: "Command"):
        """Add a subcommand to the command."""
        subcommand._parent = self
        self.subcommands.append(subcommand)

    def add_subcommands(self, subcommands: List["Command"]):
        """Add multiple subcommands to the command."""
        for subcommand in subcommands:
            subcommand._parent = self
        self.subcommands.extend(subcommands)

    def argument_by_index(self, index: int) -> Optional[Argument]:
        """Get an argument by index."""
        try:
            return self.all_arguments[index]
        except IndexError:
            return None

    def flag_to_option(self, flag: str) -> Optional[Option]:
        """Get an option by flag."""
        for option in self.all_options:
            if flag in option.flags:
                return option
        return None

    def execute(self, args: Dict[str, Any]):
        self.handler(args)
