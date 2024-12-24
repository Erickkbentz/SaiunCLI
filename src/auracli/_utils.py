from typing import List
from difflib import get_close_matches


def _is_flag(flag: str) -> bool:
    """
    Check if a string is a flag.
    """
    return _is_short_flag(flag) or _is_long_flag(flag) or _is_short_stack_flag(flag)


def _is_short_stack_flag(flag: str) -> bool:
    """
    Check if a string is a short stack flag.
    """
    return len(flag) > 2 and flag[0] == "-" and flag[1].isalpha()


def _is_short_flag(flag: str) -> bool:
    """
    Check if a string is a short flag.
    """
    return len(flag) == 2 and flag[0] == "-" and flag[1].isalpha()


def _is_long_flag(flag: str) -> bool:
    """
    Check if a string is a long flag.
    """
    return len(flag) > 2 and flag[:2] == "--" and flag[2:].isalpha()


def _split_short_stack_flag(flag: str) -> List[str]:
    """
    Split a short stack flag into individual short flags.
    """
    if not _is_short_stack_flag(flag):
        raise ValueError(f"Invalid short stack flag: {flag}")
    return [f"-{char}" for char in flag[1:]]


def _possible_commands(command: str, commands: List[str], cutoff: float = 0.6) -> List[str]:
    """
    Find possible commands based on a partial or misspelled command string.

    Args:
        command (str): The command entered by the user.
        commands (List[str]): A list of available commands.
        cutoff (float): The similarity cutoff for suggestions (default is 0.6).

    Returns:
        List[str]: A list of suggested commands that closely match the input.
    """
    return get_close_matches(command, commands, n=3, cutoff=cutoff)
