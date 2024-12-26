from typing import Any, List, Optional, Literal

from auracli._utils import _is_long_flag, _is_short_flag, _is_flag

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
        choices: Optional[List[Any]] = None,
        type: Optional[type] = str,
    ):
        """
        Initialize an Option object.

        Args:
            flags (List[str]):
                The flags to use for the option.
            message (Optional[str]):
                The help message to display for the option.
            required (Optional[bool]):
                Whether the option is required.
            action (Optional[
                Literal["store", "store_true", "store_false", "append", "extend", "count"]
            ]):
                The action to take with the option. Default is "store".
            default (Optional[str]):
                The default value for the option.
            choices (Optional[List[Any]]):
                The choices available for the option.
            type (Optional[type]):
                The type of the option.
        """
        self.flags = flags
        self.message = message
        self.required = required
        self.action = action
        self.default = default
        self.choices = choices
        self.type = type

        self._validate_flags(self.flags)

    def _validate_flags(self, flags: List[str]):
        """
        Ensure there are only 2 flags. At most 1 short flag and 1 long flag.
        """
        if len(flags) > 2:
            raise ValueError(
                f"Too many flags detected: {flags}. Only 2 flags are allowed per option."
            )

        if len(flags) == 0:
            raise ValueError(f"No flags detected: {flags}. At least 1 flag is required per option.")

        long_flags = 0
        short_flags = 0
        for flag in flags:
            if not _is_flag(flag):
                raise ValueError(
                    f"Invalid flag detected: {flag}. Flags must start with '-' or '--'."
                )
            long_flags += 1 if _is_long_flag(flag) else 0
            short_flags += 1 if _is_short_flag(flag) else 0

        if long_flags > 1:
            raise ValueError(
                f"Too many long flags detected: {flags}. "
                + "At most 1 long flag and 1 short flag are allowed per option."
            )
        if short_flags > 1:
            raise ValueError(
                f"Too many short flags detected: {flags}. "
                + "At most 1 long flag and 1 short flag are allowed per option."
            )

    @property
    def long_name(self) -> str:
        long_flag = next(flag for flag in self.flags if _is_long_flag(flag))
        if long_flag.startswith("--"):
            return long_flag[2:]
        return None

    @property
    def short_name(self) -> str:
        short_flag = next(flag for flag in self.flags if _is_short_flag(flag))
        if short_flag.startswith("-"):
            return short_flag[1:]
        return None

    def validate(self, value: Any) -> bool:
        """Validate the value of the option."""
        pass

    def parse(self, raw_value: str) -> Any:
        """Parse the raw value from the command line."""
        pass

    def handle(self, value: Optional[Any]) -> Any:
        """Handle the value of the option based on Option setup."""
        pass
