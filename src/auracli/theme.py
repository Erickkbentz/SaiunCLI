from typing import Dict, Optional

class Theme:
    BASE_THEME_FILE = ".auracli-theme"

    def __init__(
            self,
            styles: Optional[Dict[str, str]] = None,
    ):
        self.styles = styles

    @classmethod
    def load_theme(cls, theme_file: str = BASE_THEME_FILE) -> "Theme":
        import configparser
        import os

        parser = configparser.ConfigParser()
        if not os.path.exists(theme_file):
            raise FileNotFoundError(f"Theme file '{theme_file}' not found.")

        parser.read(theme_file)

        if not parser.has_section("auracli.styles"):
            raise ValueError("Invalid theme file, missing [auracli.styles] section.")
        
        styles = {
            key: value
            for key, value in parser.items("auracli.styles")
        }
        return cls(styles=styles)
