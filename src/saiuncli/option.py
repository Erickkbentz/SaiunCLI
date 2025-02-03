from typing import Any, List, Optional, Literal, Union

from saiuncli._utils import _is_long_flag, _is_short_flag, _validate_flags


class Option:
    def __init__(
        self,
        name: Optional[str] = None,
        flags: Optional[List[str]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = False,
        action: Optional[
            Literal["store", "store_true", "store_false", "append", "extend", "count"]
        ] = "store",
        default: Optional[str] = None,
        choices: Optional[List[Any]] = None,
        type: Optional[type] = str,
        nargs: Optional[Union[int, Literal["*"]]] = None,
    ):
        """
        Initialize an Option object.

        Args:
            name (Optional[str]):
                This is the name of the option. The resolved value should be referenced by
                this name in the handler. If not provided, the flag name will be used.
                If both the short and long flags are provided, the long flag name will be used.
            flags (List[str]):
                The flags to use for the option. At most 1 short flag and 1 long flag are allowed.
                If not provided, the name parameter will be used as the long flag.
            description (Optional[str]):
                The description to display for the option.
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
            nargs (Optional[Union[int, Literal["*"]]):
                The number of arguments that should be consumed.
                This is only applicable for actions - "store", "append", and "extend".
                if nargs is not None, the resolved value for the Option will be always be a list.
        """
        self.name = name
        self.flags = flags
        if not self.flags or self.name:
            raise ValueError("Either flags or name must be provided.")

        if not self.flags:
            self.flags = [f"--{self.name}"]
        if not self.name:
            self.name = self.long_name or self.short_name

        self.description = description
        self.required = required
        self.action = action
        self.default = default
        self.choices = choices
        self.type = type
        self.nargs = nargs

        _validate_flags(self.flags)

    @property
    def long_name(self) -> str:
        long_flag = next((flag for flag in self.flags if _is_long_flag(flag)), None)
        if long_flag and long_flag.startswith("--"):
            return long_flag[2:]
        return None

    @property
    def short_name(self) -> str:
        short_flag = next((flag for flag in self.flags if _is_short_flag(flag)), None)
        if short_flag and short_flag.startswith("-"):
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
