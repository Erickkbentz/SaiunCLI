from typing import Any, List, Optional, Literal

from auracli._utils import _validate_flags

_CONSTANT_UNIVERSAL_FLAGS = {
    "help": ["-h", "--help"],
    "version": ["-V", "--version"],
}

class Option:
    def __init__(
            self,
            flags: List[str],
            message: Optional[str] = None,
            required: Optional[bool] = False,
            action: Optional[
                Literal[
                    "store",
                    "store_true",
                    "store_false",
                    "append",
                    "extend",
                    "count",
                ]
            ] = "store",
            default: Optional[str] = None,
            prompt: Optional[bool] = False,
            prompt_message: Optional[str] = None,
            choices: Optional[List[Any]] = None,
            type: Optional[type] = str,
    ):
        self.flags = flags
        self.message = message
        self.required = required
        self.action = action
        self.default = default
        self.prompt = prompt
        self.prompt_message = prompt_message
        self.choices = choices
        self.type = type

        _validate_flags(self.flags)

    def validate(self, value: Any) -> bool:
        """Validate the value of the option."""
        pass

    def parse(self, raw_value: str) -> Any:
        """Parse the raw value from the command line."""
        pass
    
    def handle(self, value: Optional[Any]) -> Any:
        """Handle the value of the option based on Option setup."""
        pass

