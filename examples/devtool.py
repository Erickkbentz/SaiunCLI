from auracli import AuraCLI, Command, Option, Theme

theme = Theme()


def hello_handler(name: str, count: int):
    for i in range(count):
        print(f"Hello, {name}!")


def count_handler(a: int, b: int):
    print(f"{a} + {b} = {a + b}")


def base_handler(**args):
    print("Base command executed.")
    print(f"{args}")


if __name__ == "__main__":

    mycli = AuraCLI(
        title="My Super Cool CLI Tool",
        description="A simple tool to demonstrate auracli.",
        version="1.0.0",
        handler=base_handler,
        help_flags=[],
        version_flags=[],
        options=[
            Option(
                flags=["-v", "--verbose"],
                description="Enable verbose output.",
                action="store_true",
            ),
            Option(
                flags=["-q", "--quiet"],
                description="Enable quiet output.",
                action="store_true",
            ),
            Option(
                flags=["-d", "--debug"],
                description="Enable debug output.",
                action="store_true",
            ),
        ],
    )

    hello_command = Command(
        name="hello",
        handler=hello_handler,
        description="Prints 'Hello, world!' to the console.",
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
    )

    count_command = Command(
        name="count",
        handler=count_handler,
        description="Adds two numbers together.",
        options=[
            Option(
                flags=["-a"],
                description="The first number.",
                type=int,
                required=True,
            ),
            Option(
                flags=["-b"],
                description="The second number.",
                type=int,
                required=True,
            ),
        ],
    )

    mycli.add_subcommands([hello_command, count_command])

    mycli.run()
