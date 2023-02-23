from pathlib import Path

from .log import logger


class TemplatesRenderer():
    """For render all templates from source dir to target dir."""
    def __init__(self, templates_path: Path, target_path: Path):
        self.templates_path = templates_path
        self.target_path = target_path

    def render(self, **kwargs):
        """Render and save to target path.

        Provide variables by **kwargs.
        """
        logger.info(
            f"Render templates at {self.templates_path} to {self.target_path}")
