import pytest

from auracli import AuraCLI, Option


def dummy_handler():
    pass


@pytest.fixture
def auracli():
    return AuraCLI(
        title="My Super Cool CLI Tool",
        version="1.0.0",
        handler=dummy_handler,
        description="A simple tool to demonstrate auracli.",
        options=[
            Option(
                flags=["-v", "--verbose"],
            )
        ],
    )
