# **Overview**

[SaiunCLI](https://erickkbentz.github.io/SaiunCLI/) is a Python framework for creating visually appealing, user-friendly, and highly customizable Command-Line Interface (CLI) tools. It leverages the power of [`rich`](https://github.com/Textualize/rich?tab=readme-ov-file) for styling and formatting, making it easy to build modern CLI applications that are both functional and beautiful.

> Inspired by [rich-cli](https://github.com/Textualize/rich-cli).

![preview image](https://raw.githubusercontent.com/Erickkbentz/SaiunCLI/main/public/saiun_cli_preview.png)

## **Installation**

=== "Latest"

    ``` sh
    pip install saiuncli
    ```

=== "0.x"

    ``` sh
    pip install saiuncli=="0.*"
    ```

## **Usage**

```python
from saiuncli.cli import CLI
from saiuncli.command import Command
from saiuncli.option import Option
from saiuncli.theme import Theme

# Custom CLI Theme
theme = Theme()


# Define your command handlers
def hello_handler(name: str, count: int):
    for i in range(count):
        print(f"Hello, {name}!")

def count_handler(a: int, b: int):
    print(f"{a} + {b} = {a + b}")


def base_handler(**args):
    print("Base command executed.")
    print(f"{args}")


if __name__ == "__main__":

    # Create CLI
    mycli = CLI(
        title="My Super Cool CLI Tool",
        description="A simple tool to demonstrate saiuncli.",
        version="1.0.0",
        handler=base_handler, # Command Handler
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

    # Define Subcommands
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


    # Append Subcommands
    mycli.add_subcommands([hello_command, count_command])

    # Run your CLI Tool!
    mycli.run()

```
