# AuraCLI ✨

AuraCLI is a Python framework for creating visually appealing, user-friendly, and highly customizable Command-Line Interface (CLI) tools. It leverages the power of [`rich`](https://github.com/Textualize/rich?tab=readme-ov-file) for styling and formatting, making it easy to build modern CLI applications that are both functional and beautiful.

![preview image](https://raw.githubusercontent.com/Erickkbentz/AuraCLI/main/public/aura_cli_preview.png)

## Project Status: 🚧 Under Construction 🚧
AuraCLI is actively being developed. Some features may be incomplete or subject to change. Stay tuned for updates and improvements!

## Features

- Customizable Themes: Easily style your CLI with themes and override defaults.
- Command and Subcommand Support: Define commands and nested subcommands with specific options and arguments.
- Inherited Options and Arguments: Configure options to be inherited across subcommands.
- Global Options: Define options that apply globally across all commands and subcommands.
- Modern Styling: Leverage rich to make CLI output visually appealing, including tables, progress bars, and spinners.
- User-Friendly Argument Parsing: Parse both positional arguments and flags in a structured and intuitive manner.
- Dynamic Command Registration: Add commands programmatically during runtime.
- Configurable Help and Usage: Auto-generate help messages for commands with customization options.
- Intuitive Developer Experience: Focus on functionality without worrying about low-level details.

## Comparison with Other Tools
| Feature            | AuraCLI | Click | Argparse |
|--------------------|---------|-------|----------|
| Custom Styling     | ✅       | ❌     | ❌        |
| Nested Commands    | ✅       | ✅     | ❌        |
| Dynamic Commands   | ✅       | ✅     | ❌        |
| Option Inheritance | ✅       | ❌     | ❌        |
| Global Options     | ✅       | ❌     | ❌        |
| Easy Theming       | ✅       | ❌     | ❌        |
