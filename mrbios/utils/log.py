from rich.console import Console
from rich.prompt import Confirm
from rich.theme import Theme

custom_theme = Theme({
    "path": "italic green",
    "note": "bold magenta",
    "error": "red",
})

console = Console(theme=custom_theme)


__all__ = ["console", "Confirm"]
