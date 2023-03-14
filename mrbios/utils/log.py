from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.theme import Theme


class CustomConsole():
    """Custom console for mrbios.

    :attr use_log_as_print: console.log will call console.print.
    """

    theme = Theme({
        "path": "italic green",
        "note": "bold magenta",
        "error": "red",
    })

    def __init__(self):
        self.console = Console(theme=self.theme)
        self.use_log_as_print = False

    def log(self, msg: str = "", **kwargs):
        if self.use_log_as_print:
            self.print(msg, **kwargs)
        else:
            self.console.log(msg, **kwargs)

    def print(self, msg: str = "", **kwargs):
        self.console.print(msg, **kwargs)


console = CustomConsole()


__all__ = ["console", "Confirm", "Prompt"]
