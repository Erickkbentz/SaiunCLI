import sys
from typing import Optional, List, Dict, Any

from auracli.console import AuraConsole
from auracli.theme import Theme
from auracli.option import Option
from auracli.argument import Argument
from auracli.command import Command, _ROOT_COMMAND_NAME
from auracli._utils import _is_flag, _is_short_stack_flag, _split_short_stack_flags


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
        arguments: Optional[List[Argument]] = None,
        global_options: Optional[List[Option]] = None,
        global_arguments: Optional[List[Argument]] = None,
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
            arguments (Optional[List[Argument]]):
                The arguments available for the base CLI command
            global_options (Optional[List[Option]]):
                The global options available for the base CLI command and any subcommands.
            global_arguments (Optional[List[Argument]]):
                The global arguments available for the base CLI command and any subcommands.
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
            arguments=arguments,
            inherit_arguments=False,
            subcommands=subcommands,
        )

        self.title = title
        self.version = version
        self.theme = theme
        self.global_options = global_options or []
        self.global_arguments = global_arguments or []
        self.console = console or AuraConsole(theme=self.theme)

    def add_global_option(self, option: Option):
        self.global_options.append(option)

    def add_global_options(self, options: List[Option]):
        self.global_options.extend(options)

    def add_global_argument(self, argument: Argument):
        self.global_arguments.append(argument)

    def add_global_arguments(self, arguments: List[Argument]):
        self.global_arguments.extend(arguments)

    def display_version(self):
        pass

    def display_cli_help(self):
        pass

    def display_command_help(self, command: List[str]):
        pass

    def _flag_to_global_option(self, flag: str) -> Optional[Option]:
        for option in self.global_options:
            if flag in option.flags:
                return option
        return None

    def _process_flag(
        self, flag: str, latest_command: Command, parsed: Dict[str, Any], cli_args: List[str]
    ):
        option = latest_command.flag_to_option(flag) or self._flag_to_global_option(flag)
        if not option:
            # TODO: This should automatically display the help message
            raise ValueError(f"Invalid Option: {flag}, for available options use --help")
        flag_action = option.action

        if flag_action == "store_true":
            parsed["parsed_kwargs"][option.name] = True
        elif flag_action == "store_false":
            parsed["parsed_kwargs"][option.name] = False
        elif flag_action == "count":
            if option.name in parsed["parsed_kwargs"]:
                parsed["parsed_kwargs"][option.name] += 1
            else:
                parsed["parsed_kwargs"][option.name] = 1
        elif flag_action == "store":
            value = cli_args.pop(0)
            resolved_value = option.type(value)
            if option.choices:
                if resolved_value not in option.choices:
                    raise ValueError(f"Invalid choice: {value}, for available choices use --help")
            if option.name in parsed["parsed_kwargs"]:
                raise ValueError(f"Duplicate option: {flag}")

            if option.nargs:
                resolved_value = [resolved_value]
                if isinstance(option.nargs, int):
                    for i in range(option.nargs - 1):
                        if cli_args and not _is_flag(cli_args[0]):
                            value = cli_args.pop(0)
                            resolved_v = option.type(value)
                            if option.choices:
                                if resolved_v not in option.choices:
                                    raise ValueError(
                                        f"Invalid choice: {value}, for available choices use --help"
                                    )
                            resolved_value.append(option.type(value))
                        else:
                            raise ValueError(f"Expected {option.nargs} arguments for {flag}")
                else:
                    while cli_args and not _is_flag(cli_args[0]):
                        value = cli_args.pop(0)
                        resolved_v = option.type(value)
                        if option.choices:
                            if resolved_v not in option.choices:
                                raise ValueError(
                                    f"Invalid choice: {value}, for available choices use --help"
                                )
                        resolved_value.append(option.type(value))

            parsed["parsed_kwargs"][option.name] = resolved_value

        elif flag_action == "append":
            if option.nargs:
                resolved_value = []
                if isinstance(option.nargs, int):
                    for i in range(option.nargs):
                        if cli_args and not _is_flag(cli_args[0]):
                            value = cli_args.pop(0)
                            resolved_v = option.type(value)
                            if option.choices:
                                if resolved_v not in option.choices:
                                    raise ValueError(
                                        f"Invalid choice: {value}, for available choices use --help"
                                    )
                            resolved_value.append(option.type(value))
                        else:
                            raise ValueError(f"Expected {option.nargs} arguments for {flag}")
                else:
                    while cli_args and not _is_flag(cli_args[0]):
                        value = cli_args.pop(0)
                        resolved_v = option.type(value)
                        if option.choices:
                            if resolved_v not in option.choices:
                                raise ValueError(
                                    f"Invalid choice: {value}, for available choices use --help"
                                )
                        resolved_value.append(option.type(value))
                if option.name in parsed["parsed_kwargs"]:
                    parsed["parsed_kwargs"][option.name].append(resolved_value)
                else:
                    parsed["parsed_kwargs"][option.name] = resolved_value
            else:
                value = cli_args.pop(0)
                resolved_value = option.type(value)
                if option.choices:
                    if resolved_value not in option.choices:
                        raise ValueError(
                            f"Invalid choice: {value}, for available choices use --help"
                        )
                if option.name not in parsed["parsed_kwargs"]:
                    parsed["parsed_kwargs"][option.name] = []
                parsed["parsed_kwargs"][option.name].append(resolved_value)
        elif flag_action == "extend":
            if option.nargs:
                resolved_value = []
                if isinstance(option.nargs, int):
                    for i in range(option.nargs):
                        if cli_args and not _is_flag(cli_args[0]):
                            value = cli_args.pop(0)
                            resolved_v = option.type(value)
                            if option.choices:
                                if resolved_v not in option.choices:
                                    raise ValueError(
                                        f"Invalid choice: {value}, for available choices use --help"
                                    )
                            resolved_value.append(option.type(value))
                        else:
                            raise ValueError(f"Expected {option.nargs} arguments for {flag}")
                else:
                    while cli_args and not _is_flag(cli_args[0]):
                        value = cli_args.pop(0)
                        resolved_v = option.type(value)
                        if option.choices:
                            if resolved_v not in option.choices:
                                raise ValueError(
                                    f"Invalid choice: {value}, for available choices use --help"
                                )
                        resolved_value.append(option.type(value))
                if option.name in parsed["parsed_kwargs"]:
                    parsed["parsed_kwargs"][option.name].extend(resolved_value)
                else:
                    parsed["parsed_kwargs"][option.name] = resolved_value
            else:
                value = cli_args.pop(0)
                resolved_value = option.type(value)
                if option.choices:
                    if resolved_value not in option.choices:
                        raise ValueError(
                            f"Invalid choice: {value}, for available choices use --help"
                        )
                if option.name not in parsed["parsed_kwargs"]:
                    parsed["parsed_kwargs"][option.name] = []
                parsed["parsed_kwargs"][option.name].append(resolved_value)
        else:
            raise ValueError(f"Invalid action: {flag_action}")

    def _process_argument(
        self, arg: str, latest_command: Command, parsed: Dict[str, Any], arg_index: int
    ):
        all_arguments = self.global_arguments + latest_command.arguments
        if not all_arguments:
            raise ValueError(f"Invalid argument: {arg}")
        if arg_index >= len(all_arguments):
            raise ValueError(f"Too many arguments: {arg}")
        argument: Argument = all_arguments[arg_index]
        resolved_value = argument.type(arg)
        if argument.choices:
            if resolved_value not in argument.choices:
                raise ValueError(f"Invalid choice: {arg}, for available choices use --help")

        parsed["parsed_args"].append(resolved_value)

    def parse_cli(self) -> Dict[str, Any]:
        """Return the commands and arguments parsed from the command string.

        Returns a dictionary with the structure:

        .. code-block:: python
            {
                "commands": List[str],
                "parsed_kwargs": Dict[str, Any],
                "parsed_args": List
            }

        Returns:
            Dict[str, Any]:
                The parsed command and arguments.
        """
        parsed = {
            "commands": ["root"],
            "parsed_kwargs": {},
            "parsed_args": [],
        }
        cli_args = sys.argv[1:]

        latest_command = self
        positional_args_count = 0

        while cli_args:
            arg = cli_args.pop(0)
            if _is_flag(arg):
                if _is_short_stack_flag(arg):
                    short_flags = _split_short_stack_flags(arg)
                    arg = short_flags.pop(0)
                    cli_args = short_flags + cli_args
                self._process_flag(arg, latest_command, parsed, cli_args)
            else:
                found_command = latest_command.find_subcommand(arg)
                if found_command:
                    latest_command = found_command
                    parsed["commands"].append(arg)
                    continue
                self._process_argument(arg, latest_command, parsed, positional_args_count)
        return parsed

    def run(self, args: Optional[List[str]] = None):
        pass
