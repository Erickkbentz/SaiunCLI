import sys
from typing import Optional, List, Dict, Any

from auracli.console import AuraConsole
from auracli.theme import Theme
from auracli.option import Option
from auracli.argument import Argument
from auracli.command import Command, _ROOT_COMMAND_NAME
from auracli._utils import _is_flag, _is_short_stack_flag, _split_short_stack_flags


class ParsedCLI:
    def __init__(
        self, commands: List[str], parsed_options: Dict[str, Any], parsed_args: Dict[str, Any]
    ):
        """
        Initialize a ParsedCLI object.

        Args:
            commands (List[str]): List of commands parsed from the CLI input.
            parsed_options (Dict[str, Any]): Dictionary of option names and their values.
            parsed_args (Dict[str, Any]): Dictionary of argument names and their values.
        """
        self.commands = commands
        self.parsed_options = parsed_options
        self.parsed_args = parsed_args

    def __repr__(self):
        """String representation for debugging."""
        repr = "<ParsedCLI(commands=%s, parsed_options=%s, parsed_args=%s" % (
            self.commands,
            self.parsed_options,
            self.parsed_args,
        )
        for key, value in self.parsed_options.items():
            repr += f", {key}={value}"
        for key, value in self.parsed_args.items():
            repr += f", {key}={value}"
        repr += ")>"
        return repr

    def __getattr__(self, name: str):
        """
        Allow direct access to `parsed_options` or `parsed_args` values as attributes.
        """
        if name in self.parsed_options:
            return self.parsed_options[name]
        if name in self.parsed_args:
            return self.parsed_args[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")


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

        Operations for displaying "help" and "version" information are handled automatically
        and reserve the flags ["--help", "-h"] and ["--version", "-V"] respectively.

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
            parsed["parsed_options"][option.name] = True
        elif flag_action == "store_false":
            parsed["parsed_options"][option.name] = False
        elif flag_action == "count":
            if option.name in parsed["parsed_options"]:
                parsed["parsed_options"][option.name] += 1
            else:
                parsed["parsed_options"][option.name] = 1
        elif flag_action == "store":
            value = cli_args.pop(0)
            resolved_value = option.type(value)
            if option.choices:
                if resolved_value not in option.choices:
                    raise ValueError(f"Invalid choice: {value}, for available choices use --help")
            if option.name in parsed["parsed_options"]:
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

            parsed["parsed_options"][option.name] = resolved_value

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
                if option.name in parsed["parsed_options"]:
                    parsed["parsed_options"][option.name].append(resolved_value)
                else:
                    parsed["parsed_options"][option.name] = resolved_value
            else:
                value = cli_args.pop(0)
                resolved_value = option.type(value)
                if option.choices:
                    if resolved_value not in option.choices:
                        raise ValueError(
                            f"Invalid choice: {value}, for available choices use --help"
                        )
                if option.name not in parsed["parsed_options"]:
                    parsed["parsed_options"][option.name] = []
                parsed["parsed_options"][option.name].append(resolved_value)
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
                if option.name in parsed["parsed_options"]:
                    parsed["parsed_options"][option.name].extend(resolved_value)
                else:
                    parsed["parsed_options"][option.name] = resolved_value
            else:
                value = cli_args.pop(0)
                resolved_value = option.type(value)
                if option.choices:
                    if resolved_value not in option.choices:
                        raise ValueError(
                            f"Invalid choice: {value}, for available choices use --help"
                        )
                if option.name not in parsed["parsed_options"]:
                    parsed["parsed_options"][option.name] = []
                parsed["parsed_options"][option.name].append(resolved_value)
        else:
            raise ValueError(f"Invalid action: {flag_action}")

    def _process_argument(
        self, arg: str, latest_command: Command, parsed: Dict[str, Any], arg_index: int
    ):
        all_arguments = self.global_arguments + latest_command.all_arguments
        if not all_arguments:
            raise ValueError(f"Invalid argument: {arg}")
        if arg_index >= len(all_arguments):
            raise ValueError(f"Too many arguments: {arg}")
        argument: Argument = all_arguments[arg_index]
        resolved_value = argument.type(arg)
        if argument.choices:
            if resolved_value not in argument.choices:
                raise ValueError(f"Invalid choice: {arg}, for available choices use --help")

        parsed["parsed_args"][argument.name] = resolved_value

    def _set_defaults_for_command(self, command: Command, parsed: Dict[str, Any]):
        for option in command.all_options:
            if option.default and option.name not in parsed["parsed_options"]:
                parsed["parsed_options"][option.name] = option.default

        for argument in command.all_arguments:
            if argument.default and len(parsed["parsed_args"]) < len(command.all_arguments):
                parsed["parsed_args"][argument.name] = argument.default

    def parse_cli(self) -> ParsedCLI:
        """Return the commands and arguments parsed from the command string.

        Returns:
            ParsedCLI: The parsed commands and arguments.
        """
        parsed = {
            "commands": ["root"],
            "parsed_options": {},
            "parsed_args": {},
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
                positional_args_count += 1

        return ParsedCLI(
            commands=parsed["commands"],
            parsed_options=parsed["parsed_options"],
            parsed_args=parsed["parsed_args"],
        )

    def run(self, args: Optional[List[str]] = None):
        pass
