from auracli import Option, Command, Argument, ParsedCLI


def dummy_handler():
    pass


PARSE_CLI_HAPPY_CASE_TESTS = {
    "cases": [
        # Test Case 0 - Root Only
        {
            "command": ["root"],
            "expected_parse_cli": ParsedCLI(
                commands=["root"],
                parsed_options={},
                parsed_args={},
                help=False,
                version=False,
            ),
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
            "command": ["root", "subcommand"],
            "expected_parse_cli": ParsedCLI(
                commands=["root", "subcommand"],
                parsed_options={},
                parsed_args={},
                help=False,
                version=False,
            ),
        },
        # Test Case 2 - Root with Global Option
        {
            "cli_global_options": [
                Option(
                    flags=["-v", "--verbose"],
                    description="Enable verbose output.",
                    action="store_true",
                )
            ],
            "command": ["root", "-v"],
            "expected_parse_cli": ParsedCLI(
                commands=["root"],
                parsed_options={"verbose": True},
                parsed_args={},
                help=False,
                version=False,
            ),
        },
        # Test Case 3 - Root with Global Argument
        {
            "cli_global_arguments": [
                Argument(
                    name="arg1",
                    description="An argument.",
                )
            ],
            "command": ["root", "val1"],
            "expected_parse_cli": ParsedCLI(
                commands=["root"],
                parsed_options={},
                parsed_args={"arg1": "val1"},
                help=False,
                version=False,
            ),
        },
        # Test Case 4 - Root with Options
        {
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
            "command": ["root", "--name", "Alice", "--count", "3"],
            "expected_parse_cli": ParsedCLI(
                commands=["root"],
                parsed_options={"name": "Alice", "count": 3},
                parsed_args={},
                help=False,
                version=False,
            ),
        },
        # Test Case 5 - Root with Arguments
        {
            "cli_args": [
                Argument(
                    name="arg1",
                    description="An argument.",
                ),
                Argument(
                    name="arg2",
                    description="Another argument.",
                ),
            ],
            "command": ["root", "val1", "val2"],
            "expected_parse_cli": ParsedCLI(
                commands=["root"],
                parsed_options={},
                parsed_args={"arg1": "val1", "arg2": "val2"},
                help=False,
                version=False,
            ),
        },
        # Test Case 6 - Root with Global Option, Global Argument, Options, and Arguments
        {
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
                Argument(
                    name="arg3",
                    description="Another argument.",
                ),
            ],
            "command": ["root", "-v", "--name", "Alice", "--count", "3", "val1", "val2", "val3"],
            "expected_parse_cli": ParsedCLI(
                commands=["root"],
                parsed_options={"verbose": True, "name": "Alice", "count": 3},
                parsed_args={"arg1": "val1", "arg2": "val2", "arg3": "val3"},
                help=False,
                version=False,
            ),
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
                        Argument(
                            name="arg3",
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
            "command": [
                "root",
                "subcommand",
                "-v",
                "--name",
                "Alice",
                "--count",
                "3",
                "val1",
                "val2",
                "val3",
            ],
            "expected_parse_cli": ParsedCLI(
                commands=["root", "subcommand"],
                parsed_options={"verbose": True, "name": "Alice", "count": 3},
                parsed_args={"arg1": "val1", "arg2": "val2", "arg3": "val3"},
                help=False,
                version=False,
            ),
        },
        # Test Case 8 - Short Stacked Flags
        {
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
            "command": ["root", "-vqdD"],
            "expected_parse_cli": ParsedCLI(
                commands=["root"],
                parsed_options={"v": True, "q": True, "d": True, "D": False},
                parsed_args={},
                help=False,
                version=False,
            ),
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
                        Argument(
                            name="arg2",
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
                                Argument(
                                    name="arg4",
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
                "val0",
                "val1",
                "val2",
                "val3",
                "val4",
            ],
            "expected_parse_cli": ParsedCLI(
                commands=["root", "subcommand1", "subcommand2"],
                parsed_options={"v": True, "flag": "value", "name": "Alice", "count": 3},
                parsed_args={
                    "arg0": "val0",
                    "arg1": "val1",
                    "arg2": "val2",
                    "arg3": "val3",
                    "arg4": "val4",
                },
                help=False,
                version=False,
            ),
        },
    ],
    "ids": [
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
}
