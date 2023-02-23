from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "path": "italic green",
    "note": "bold magenta",
})

console = Console(theme=custom_theme)
