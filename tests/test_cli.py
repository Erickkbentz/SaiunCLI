import pytest
from unittest.mock import patch

from auracli import AuraCLI

from .data import (
    dummy_handler,
    PARSE_CLI_HAPPY_CASE_TESTS,
)


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
    PARSE_CLI_HAPPY_CASE_TESTS["cases"],
    ids=PARSE_CLI_HAPPY_CASE_TESTS["ids"],
)
@patch("sys.argv", new_callable=list)
def test_parse_command_happy_cases(mock_argv, test_case, auracli: AuraCLI):
    if test_case.get("cli_subcommands"):
        for subcommand in test_case["cli_subcommands"]:
            auracli.add_subcommand(subcommand)
    if test_case.get("cli_global_options"):
        for global_option in test_case["cli_global_options"]:
            auracli.add_global_option(global_option)
    if test_case.get("cli_global_arguments"):
        for global_argument in test_case["cli_global_arguments"]:
            auracli.add_global_argument(global_argument)
    if test_case.get("cli_options"):
        for option in test_case["cli_options"]:
            auracli.add_option(option)
    if test_case.get("cli_args"):
        for arg in test_case["cli_args"]:
            auracli.add_argument(arg)

    command = test_case.get("command")
    mock_argv.extend(command)

    parsed_cli = auracli.parse_cli()

    assert parsed_cli.__dict__ == test_case["expected_parse_cli"].__dict__
