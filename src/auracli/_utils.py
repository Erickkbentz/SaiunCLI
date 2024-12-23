from typing import List, Dict
from difflib import get_close_matches

from auracli import Option

def _validate_options(options: List[Option]):
        """
        Ensure there are no duplicate flags across all options.
        """
        flag_set = set()
        for option in options:
            for flag in option.flags:
                if flag in flag_set:
                    raise ValueError(f"Duplicate flag detected: {flag}. Flags must be unique between commands.")
                flag_set.add(flag)

def _is_flag(flag: str) -> bool:
    """
    Check if a string is a flag.
    """
    return flag.startswith("-") or flag.startswith("--")

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
