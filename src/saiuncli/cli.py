import os
import sys
from typing import Optional, List, Dict, Any

from rich.text import Text

from saiuncli._constants import _ROOT_COMMAND_NAME, _HELP_NAME, _VERSION_NAME, _GLOBAL_FLAGS
from saiuncli.option import Option
from saiuncli.argument import Argument
from saiuncli.command import Command
from saiuncli.console import Console

from saiuncli._utils import (
    _is_flag,
    _is_short_stack_flag,
    _split_short_stack_flags,
    _validate_flags,
)


class ParsedCLI:
    def __init__(
        self,
        commands: List[str],
        parsed_options: Dict[str, Any],
        parsed_args: Dict[str, Any],
        help: bool = False,
        version: bool = False,
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
        self.help = help
        self.version = version

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

    def handler_kwargs_dict(self):
        return {**self.parsed_options, **self.parsed_args}


class CLI(Command):
    def __init__(
        self,
        title: str,
        version: Optional[str] = None,
        console: Optional[Console] = None,
        handler: Optional[callable] = None,
        description: Optional[str] = None,
        usage: Optional[str] = None,
        options: Optional[List[Option]] = None,
        arguments: Optional[List[Argument]] = None,
        help_flags: Optional[List[str]] = None,
        version_flags: Optional[List[str]] = None,
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
            console (Optional[Console]):
                The Console object to use for displaying outputs for the CLI tool.
            handler (Optional[callable]):
                The function to execute when the base CLI command is called.
                If not provided, root command will only display help and version information.
            description (Optional[str]):
                The description of the base CLI command.
            usage (Optional[str]):
                The usage information for the base CLI command.
                Defaults to "[SUBCOMMANDS][OPTIONS][ARGUMENTS]" if not provided.
            options (Optional[List[Option]]):
                The options available for the base CLI command.
            arguments (Optional[List[Argument]]):
                The arguments available for the base CLI command
            help_flags (Optional[List[str]]):
                The flag overrides for CLI help operation.
                Defaults to ["-h", "--help"] if not provided.
            version_flags (Optional[List[str]]):
                The flag overrides for CLI version operation.
                Defaults to ["-V", "--version"] if not provided.
            global_options (Optional[List[Option]]):
                The global options available for the base CLI command and any subcommands.
            global_arguments (Optional[List[Argument]]):
                The global arguments available for the base CLI command and any subcommands.
            subcommands (Optional[List[Command]]):
                The subcommands available for the base CLI command.
        """
        self.version_flags = version_flags or _GLOBAL_FLAGS[_VERSION_NAME]
        self.help_flags = help_flags or _GLOBAL_FLAGS[_HELP_NAME]
        _validate_flags(self.help_flags)
        _validate_flags(self.version_flags)
        if any(flag in self.help_flags for flag in self.version_flags):
            raise ValueError("Duplicate flags detected for help and version operations.")

        super().__init__(
            name=_ROOT_COMMAND_NAME,
            handler=handler,
            description=description,
            usage=usage,
            options=options,
            inherit_options=False,
            arguments=arguments,
            inherit_arguments=False,
            subcommands=subcommands,
        )
        self.title = title
        self.version = version
        self.global_options = global_options or []
        self.global_arguments = global_arguments or []
        self._cli_command = ""
        self.console = console or Console()

    def add_global_option(self, option: Option):
        self.global_options.append(option)

    def add_global_options(self, options: List[Option]):
        self.global_options.extend(options)

    def add_global_argument(self, argument: Argument):
        self.global_arguments.append(argument)

    def add_global_arguments(self, arguments: List[Argument]):
        self.global_arguments.extend(arguments)

    def _flag_to_global_option(self, flag: str) -> Optional[Option]:
        for option in self.global_options:
            if flag in option.flags:
                return option
        return None

    def _process_flag(
        self, flag: str, latest_command: Command, parsed: Dict[str, Any], cli_args: List[str]
    ):
        if flag in self.help_flags:
            parsed[_HELP_NAME] = True
            return

        if flag in self.version_flags:
            parsed[_VERSION_NAME] = True
            return

        option = latest_command.flag_to_option(flag) or self._flag_to_global_option(flag)
        if not option:
            error = Text(f"Invalid option '{flag}'")
            self._cli_error(error, command=latest_command)

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
                    error = Text(f"Invalid choice '{value}'")
                    self._cli_error(error, command=latest_command)

            if option.name in parsed["parsed_options"]:
                error = Text(f"Duplicate option '{flag}'.")
                self._cli_error(error, command=latest_command)

            if option.nargs:
                resolved_value = [resolved_value]
                if isinstance(option.nargs, int):
                    for i in range(option.nargs - 1):
                        if cli_args and not _is_flag(cli_args[0]):
                            value = cli_args.pop(0)
                            resolved_v = option.type(value)
                            if option.choices:
                                if resolved_v not in option.choices:
                                    error = Text(f"Invalid choice '{value}'")
                                    self._cli_error(error, command=latest_command)
                            resolved_value.append(option.type(value))
                        else:
                            error = Text(f"Expected '{option.nargs}' arguments for {flag}")
                            self._cli_error(error, command=latest_command)

                else:
                    while cli_args and not _is_flag(cli_args[0]):
                        value = cli_args.pop(0)
                        resolved_v = option.type(value)
                        if option.choices:
                            if resolved_v not in option.choices:
                                error = Text(f"Invalid choice '{value}'")
                                self._cli_error(error, command=latest_command)
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
                                    error = Text(f"Invalid choice '{value}'")
                                    self._cli_error(error, command=latest_command)
                            resolved_value.append(option.type(value))
                        else:
                            error = Text(f"Expected {option.nargs} arguments for '{flag}'")
                            self._cli_error(error, command=latest_command)
                else:
                    while cli_args and not _is_flag(cli_args[0]):
                        value = cli_args.pop(0)
                        resolved_v = option.type(value)
                        if option.choices:
                            if resolved_v not in option.choices:
                                error = Text(f"Invalid choice '{value}'")
                                self._cli_error(error, command=latest_command)
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
                        error = Text(f"Invalid choice '{value}'")
                        self._cli_error(error, command=latest_command)
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
                                    error = Text(f"Invalid choice '{value}'")
                                    self._cli_error(error, command=latest_command)
                            resolved_value.append(option.type(value))
                        else:
                            error = Text(f"Expected '{option.nargs}' arguments for {flag}")
                            self._cli_error(error, command=latest_command)
                else:
                    while cli_args and not _is_flag(cli_args[0]):
                        value = cli_args.pop(0)
                        resolved_v = option.type(value)
                        if option.choices:
                            if resolved_v not in option.choices:
                                error = Text(f"Invalid choice '{value}'")
                                self._cli_error(error, command=latest_command)
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
                        error = Text(f"Invalid choice '{value}'")
                        self._cli_error(error, command=latest_command)
                if option.name not in parsed["parsed_options"]:
                    parsed["parsed_options"][option.name] = []
                parsed["parsed_options"][option.name].append(resolved_value)
        else:
            error = Text(f"Invalid action '{flag_action}'")
            self._cli_error(error, command=latest_command)

    def _process_argument(
        self, arg: str, latest_command: Command, parsed: Dict[str, Any], arg_index: int
    ):
        all_arguments = self.global_arguments + latest_command.all_arguments
        if not all_arguments:
            error = Text(f"Invalid argument '{arg}'")
            self._cli_error(error, command=latest_command)
        if arg_index >= len(all_arguments):
            error = Text(f"Too many arguments '{arg}'")
            self._cli_error(error, command=latest_command)
        argument: Argument = all_arguments[arg_index]
        resolved_value = argument.type(arg)
        if argument.choices:
            if resolved_value not in argument.choices:
                error = Text(f"Invalid choice '{arg}'")
                self._cli_error(error, command=latest_command)

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
            _VERSION_NAME: False,
            _HELP_NAME: False,
        }
        self._cli_command = os.path.basename(sys.argv[0])
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

        self._set_defaults_for_command(latest_command, parsed)

        return ParsedCLI(
            commands=parsed["commands"],
            parsed_options=parsed["parsed_options"],
            parsed_args=parsed["parsed_args"],
            help=parsed[_HELP_NAME],
            version=parsed[_VERSION_NAME],
        )

    def _cli_error(self, error: str, command: Optional[Command] = None):
        """Display an error message and exit the CLI tool."""
        if error is None or error == "":
            error = "An unknown error occurred."
        self.console.print(f"[bold red]Error:[/bold red] {error}\n")
        self.display_help(command=command, header=False)
        sys.exit(1)

    def _full_usage_string(self, command: Optional[Command]) -> str:
        """Generate the full usage string for a command."""
        if not command:
            command = self
        commands_string = f"{self._cli_command} "
        current_command = command
        subcommand_string = ""
        while current_command and current_command.name != _ROOT_COMMAND_NAME:
            subcommand_string += f"{current_command.name} " + subcommand_string
            current_command = current_command._parent
        commands_string += subcommand_string.strip()
        return f"{commands_string} {current_command.usage}"

    def display_help(self, command: Optional[Command] = None, header: bool = True):
        """Display help information for the CLI tool.

        Args:
            command (Command):
                The command to display help for.
        """
        if not command:
            command = self
        cli_usage = self._full_usage_string(command)
        self.console.display_help(
            title=self.title,
            description=command.description,
            version=self.version,
            usage=cli_usage,
            options=command.all_options + self.global_options,
            arguments=command.all_arguments + self.global_arguments,
            subcommands=command.subcommands,
            show_header=header,
            version_flags=self.version_flags,
            help_flags=self.help_flags,
        )

    def run(self, parsed_cli: Optional[ParsedCLI] = None):
        """Executes CLI tool based handlers, options, and arguments in
            the ParsedCLI.


        Args:
            parsed_cli (Optional[ParsedCLI]):
                If not provided, CLI will be parsed by calling `self.parse_cli()`
        """
        parsed_cli = parsed_cli or self.parse_cli()
        command_name = parsed_cli.commands[-1]

        if command_name == _ROOT_COMMAND_NAME:
            command = self
        else:
            command = self.find_subcommand(command_name)

        if parsed_cli.help or not command.handler:
            self.display_help(command)
            return
        if parsed_cli.version:
            self.console.display_version(self.version)
            return

        missing_required_options = [
            option.name
            for option in command.all_options + self.global_options
            if option.required and option.name not in parsed_cli.parsed_options
        ]
        if missing_required_options:
            error = Text(f"Missing required options: {', '.join(missing_required_options)}")
            self._cli_error(error, command=command)

        missing_required_arguments = [
            argument.name
            for argument in command.all_arguments + self.global_arguments
            if argument.required and argument.name not in parsed_cli.parsed_args
        ]
        if missing_required_arguments:
            error = Text(f"Missing required arguments: {', '.join(missing_required_arguments)}")
            self._cli_error(error, command=command)

        kwargs = parsed_cli.handler_kwargs_dict()
        try:
            command.handler(**kwargs)
        except Exception as e:
            self._cli_error(str(e), command=command)
