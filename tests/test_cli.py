import pytest
from unittest.mock import patch

from auracli import AuraCLI, Option, Command


def dummy_handler():
    pass


@pytest.fixture
def auracli():
    return AuraCLI(
        title="My Super Cool CLI Tool",
        version="1.0.0",
        handler=dummy_handler,
        description="A simple tool to demonstrate auracli.",
        global_options=[
            Option(
                flags=["-v", "--verbose"],
            )
        ],
    )


def test_auracli(auracli: AuraCLI):
    assert auracli.title == "My Super Cool CLI Tool"
    assert auracli.version == "1.0.0"
    assert auracli.handler == dummy_handler


@patch("sys.argv", new_callable=list)
def test_parse_command(mock_argv, auracli: AuraCLI):
    auracli.add_subcommand(
        Command(
            name="count",
            handler=dummy_handler,
            options=[
                Option(
                    flags=["-a"],
                    type=int,
                ),
                Option(
                    flags=["-b"],
                    type=int,
                ),
            ],
        )
    )

    command = ["root", "count", "-a", "1", "-b", "2"]
    mock_argv.extend(command)

    parsed_command = auracli.parse_cli()
    expected_parsed_command = {
        "commands": ["root", "count"],
        "parsed_kwargs": {
            "a": 1,
            "b": 2,
        },
        "parsed_args": [],
    }

    assert parsed_command == expected_parsed_command
