from auracli import AuraCLI, AuraConsole, Command, Option, Theme

theme = Theme()
console = AuraConsole(theme=theme)


def hello_handler(name: str, count: int):
    for i in range(count):
        console.print(f"Hello, {name}!")


def count_handler(a: int, b: int):
    console.print(f"{a} + {b} = {a + b}")


def base_handler(args):
    console.print("Base command executed.")
    console.print(args)


if __name__ == "__main__":

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

    mycli = AuraCLI(
        title="My Super Cool CLI Tool",
        description="A simple tool to demonstrate auracli.",
        version="1.0.0",
        console=console,
        handler=base_handler,
        subcommands=[hello_command, count_command],
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

    mycli.run()
