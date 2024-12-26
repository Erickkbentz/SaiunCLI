import pytest
from unittest.mock import patch

from auracli import AuraCLI, Option, Command, Argument


def dummy_handler():
    pass


@pytest.fixture(scope="function")
def auracli():
    return AuraCLI(
        title="My Super Cool CLI Tool",
        version="1.0.0",
        handler=dummy_handler,
        description="A simple tool to demonstrate auracli.",
    )


def test_auracli(auracli: AuraCLI):
    assert auracli.title == "My Super Cool CLI Tool"
    assert auracli.version == "1.0.0"
    assert auracli.handler == dummy_handler


@pytest.mark.parametrize(
    "test_case",
    [
        # Test Case 0 - Root Only
        {
            "cli_subcommands": [],
            "cli_global_options": [],
            "cli_global_arguments": [],
            "cli_options": [],
            "cli_args": [],
            "command": ["root"],
            "expected_parse_cli": {
                "commands": ["root"],
                "parsed_kwargs": {},
                "parsed_args": [],
            },
        },
        # Test Case 1 - Subcommand
        {
            "cli_subcommands": [
                Command(
                    name="subcommand",
                    handler=dummy_handler,
                    description="A subcommand.",
                )
            ],
            "cli_global_options": [],
            "cli_global_arguments": [],
            "cli_options": [],
            "cli_args": [],
            "command": ["root", "subcommand"],
            "expected_parse_cli": {
                "commands": ["root", "subcommand"],
                "parsed_kwargs": {},
                "parsed_args": [],
            },
        },
        # Test Case 2 - Root with Global Option
        {
            "cli_subcommands": [],
            "cli_global_options": [
                Option(
                    flags=["-v", "--verbose"],
                    description="Enable verbose output.",
                    action="store_true",
                )
            ],
            "cli_global_arguments": [],
            "cli_options": [],
            "cli_args": [],
            "command": ["root", "-v"],
            "expected_parse_cli": {
                "commands": ["root"],
                "parsed_kwargs": {"verbose": True},
                "parsed_args": [],
            },
        },
        # Test Case 3 - Root with Global Argument
        {
            "cli_subcommands": [],
            "cli_global_options": [],
            "cli_global_arguments": [
                Argument(
                    name="arg1",
                    description="An argument.",
                )
            ],
            "cli_options": [],
            "cli_args": [],
            "command": ["root", "arg1"],
            "expected_parse_cli": {
                "commands": ["root"],
                "parsed_kwargs": {},
                "parsed_args": ["arg1"],
            },
        },
        # Test Case 4 - Root with Options
        {
            "cli_subcommands": [],
            "cli_global_options": [],
            "cli_global_arguments": [],
            "cli_options": [
                Option(
                    flags=["-n", "--name"],
                    description="The name to print.",
                    type=str,
                    required=True,
                ),
                Option(
                    flags=["-c", "--count"],
                    description="The number of times to print the name.",
                    type=int,
                    default=1,
                ),
            ],
            "cli_args": [],
            "command": ["root", "--name", "Alice", "--count", "3"],
            "expected_parse_cli": {
                "commands": ["root"],
                "parsed_kwargs": {"name": "Alice", "count": 3},
                "parsed_args": [],
            },
        },
        # Test Case 5 - Root with Arguments
        {
            "cli_subcommands": [],
            "cli_global_options": [],
            "cli_global_arguments": [],
            "cli_options": [],
            "cli_args": [
                Argument(
                    name="arg1",
                    description="An argument.",
                ),
                Command(
                    name="arg2",
                    handler=dummy_handler,
                    description="Another argument.",
                ),
            ],
            "command": ["root", "arg1", "arg2"],
            "expected_parse_cli": {
                "commands": ["root"],
                "parsed_kwargs": {},
                "parsed_args": ["arg1", "arg2"],
            },
        },
        # Test Case 6 - Root with Global Option, Global Argument, Options, and Arguments
        {
            "cli_subcommands": [],
            "cli_global_options": [
                Option(
                    flags=["-v", "--verbose"],
                    description="Enable verbose output.",
                    action="store_true",
                )
            ],
            "cli_global_arguments": [
                Argument(
                    name="arg1",
                    description="An argument.",
                )
            ],
            "cli_options": [
                Option(
                    flags=["-n", "--name"],
                    description="The name to print.",
                    type=str,
                    required=True,
                ),
                Option(
                    flags=["-c", "--count"],
                    description="The number of times to print the name.",
                    type=int,
                    default=1,
                ),
            ],
            "cli_args": [
                Argument(
                    name="arg2",
                    description="An argument.",
                ),
                Command(
                    name="arg3",
                    handler=dummy_handler,
                    description="Another argument.",
                ),
            ],
            "command": ["root", "-v", "--name", "Alice", "--count", "3", "arg1", "arg2", "arg3"],
            "expected_parse_cli": {
                "commands": ["root"],
                "parsed_kwargs": {"verbose": True, "name": "Alice", "count": 3},
                "parsed_args": ["arg1", "arg2", "arg3"],
            },
        },
        # Test Case 7 - Subcommand with Global Option, Global Argument, Options, and Arguments
        {
            "cli_subcommands": [
                Command(
                    name="subcommand",
                    handler=dummy_handler,
                    description="A subcommand.",
                    options=[
                        Option(
                            flags=["-n", "--name"],
                            description="The name to print.",
                            type=str,
                            required=True,
                        ),
                        Option(
                            flags=["-c", "--count"],
                            description="The number of times to print the name.",
                            type=int,
                            default=1,
                        ),
                    ],
                    arguments=[
                        Argument(
                            name="arg2",
                            description="An argument.",
                        ),
                        Command(
                            name="arg3",
                            handler=dummy_handler,
                            description="Another argument.",
                        ),
                    ],
                )
            ],
            "cli_global_options": [
                Option(
                    flags=["-v", "--verbose"],
                    description="Enable verbose output.",
                    action="store_true",
                )
            ],
            "cli_global_arguments": [
                Argument(
                    name="arg1",
                    description="An argument.",
                )
            ],
            "cli_options": [],
            "cli_args": [],
            "command": [
                "root",
                "subcommand",
                "-v",
                "--name",
                "Alice",
                "--count",
                "3",
                "arg1",
                "arg2",
                "arg3",
            ],
            "expected_parse_cli": {
                "commands": ["root", "subcommand"],
                "parsed_kwargs": {"verbose": True, "name": "Alice", "count": 3},
                "parsed_args": ["arg1", "arg2", "arg3"],
            },
        },
        # Test Case 8 - Short Stacked Flags
        {
            "cli_subcommands": [],
            "cli_global_options": [
                Option(
                    flags=["-v"],
                    description="Enable verbose output.",
                    action="store_true",
                ),
                Option(
                    flags=["-q"],
                    description="Enable quiet output.",
                    action="store_true",
                ),
                Option(
                    flags=["-d"],
                    description="Enable debug output.",
                    action="store_true",
                ),
                Option(
                    flags=["-D"],
                    description="Disable development mode.",
                    action="store_false",
                ),
            ],
            "cli_global_arguments": [],
            "cli_options": [],
            "cli_args": [],
            "command": ["root", "-vqdD"],
            "expected_parse_cli": {
                "commands": ["root"],
                "parsed_kwargs": {"v": True, "q": True, "d": True, "D": False},
                "parsed_args": [],
            },
        },
        # Test Case 9 - Multiple Nested Subcommands with Inheritance
        {
            "cli_subcommands": [
                Command(
                    name="subcommand1",
                    handler=dummy_handler,
                    description="A subcommand.",
                    options=[
                        Option(
                            flags=["-n", "--name"],
                            description="The name to print.",
                            type=str,
                            required=True,
                        ),
                        Option(
                            flags=["-c", "--count"],
                            description="The number of times to print the name.",
                            type=int,
                            default=1,
                        ),
                    ],
                    arguments=[
                        Argument(
                            name="arg1",
                            description="An argument.",
                        ),
                        Command(
                            name="arg2",
                            handler=dummy_handler,
                            description="Another argument.",
                        ),
                    ],
                    subcommands=[
                        Command(
                            name="subcommand2",
                            handler=dummy_handler,
                            description="Another subcommand.",
                            inherit_options=True,
                            inherit_arguments=True,
                            options=[
                                Option(
                                    flags=["-f", "--flag"],
                                    description="A flag.",
                                )
                            ],
                            arguments=[
                                Argument(
                                    name="arg3",
                                    description="An argument.",
                                ),
                                Command(
                                    name="arg4",
                                    handler=dummy_handler,
                                    description="Another argument.",
                                ),
                            ],
                        )
                    ],
                )
            ],
            "cli_global_options": [
                Option(
                    flags=["-v"],
                    description="Enable verbose output.",
                    action="store_true",
                )
            ],
            "cli_global_arguments": [
                Argument(
                    name="arg0",
                    description="An argument.",
                )
            ],
            "cli_options": [],
            "cli_args": [],
            "command": [
                "root",
                "subcommand1",
                "subcommand2",
                "-v",
                "-f",
                "value",
                "--name",
                "Alice",
                "--count",
                "3",
                "arg0",
                "arg1",
                "arg2",
                "arg3",
                "arg4",
            ],
            "expected_parse_cli": {
                "commands": ["root", "subcommand1", "subcommand2"],
                "parsed_kwargs": {"v": True, "flag": "value", "name": "Alice", "count": 3},
                "parsed_args": ["arg0", "arg1", "arg2", "arg3", "arg4"],
            },
        },
    ],
    ids=[
        "root_only",
        "subcommand",
        "root_with_global_option",
        "root_with_global_argument",
        "root_with_options",
        "root_with_arguments",
        "root_with_globals_and_options_and_arguments",
        "subcommand_with_globals_and_options_arguments",
        "short_stacked_flags",
        "multiple_nested_subcommands_with_inheritance",
    ],
)
@patch("sys.argv", new_callable=list)
def test_parse_command_happy_cases(mock_argv, test_case, auracli: AuraCLI):
    if test_case["cli_subcommands"]:
        for subcommand in test_case["cli_subcommands"]:
            auracli.add_subcommand(subcommand)
    if test_case["cli_global_options"]:
        for global_option in test_case["cli_global_options"]:
            auracli.add_global_option(global_option)
    if test_case["cli_global_arguments"]:
        for global_argument in test_case["cli_global_arguments"]:
            auracli.add_global_argument(global_argument)
    if test_case["cli_options"]:
        for option in test_case["cli_options"]:
            auracli.add_option(option)
    if test_case["cli_args"]:
        for arg in test_case["cli_args"]:
            auracli.add_argument(arg)

    command = test_case["command"]
    mock_argv.extend(command)

    parsed_cli = auracli.parse_cli()

    assert parsed_cli == test_case["expected_parse_cli"]
