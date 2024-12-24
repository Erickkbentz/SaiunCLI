import logging

from typing import Any, Dict, List, Optional
from rich.console import Console
from auracli import Theme


class AuraConsole:
    def __init__(
        self,
        theme: Optional[Theme] = None,
    ):
        self.theme = theme
        self.console = Console()
        self.logger = self._setup_logging()

    def _setup_logging(self, logger_name: Optional[str] = "auracli") -> logging.Logger:
        return logging.getLogger(logger_name)

    def log(self, message: str, level: Optional[int] = logging.INFO, style: Optional[str] = None):
        if style:
            message = f"[{style}]{message}[/{style}]"
        self.console.log(message)
        self.logger.log(level, message)

    def error(self, message: str):
        self.log(message, level=logging.ERROR, style="bold red")

    def debug(self, message: str):
        self.log(message, level=logging.DEBUG, style="dim")

    def info(self, message: str):
        self.log(message, level=logging.INFO, style="green")

    def warning(self, message: str):
        self.log(message, level=logging.WARNING, style="yellow")

    def print(self, message: str):
        self.console.print(message)

    def print_table(self, data: List[Dict[str, Any]]):
        pass

    def print_json(self, data: Dict[str, Any]):
        pass

    def print_yaml(self, data: Dict[str, Any]):
        pass

    def progress(self, message: str):
        pass

    def spinner(self, message: str):
        pass
