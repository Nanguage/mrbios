import typing as T
from pathlib import Path

from ..utils.log import console
from ..utils.misc import (
    TemplatesRenderer, ENV_TEMPLATES_PATH,
    TEMPLATES_PATH
)
from .env import Env


def list_env_templates() -> list[str]:
    return [
        str(i.name) for i in ENV_TEMPLATES_PATH.glob("*")
    ]


class SubPaths(T.NamedTuple):
    """Project's sub-paths."""
    env: Path
    task: Path
    pipe: Path
    format: Path


class Project():
    """Abscraction of the project."""
    def __init__(self, path: str):
        p = Path(path)
        self.path = p

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def sub_paths(self) -> SubPaths:
        p = self.path
        return SubPaths(
            p / "Environments",
            p / "Tasks",
            p / "Pipelines",
            p / "Formats",
        )

    def create(self):
        """Create the project."""
        console.log(
            f"Create project at: [path]{self.path.absolute()}[/path]")
        p = self.path
        if not p.exists():
            p.mkdir(parents=True)
        for sub in self.sub_paths:
            if not sub.exists():
                sub.mkdir(parents=True)
        # copy files
        renderer = TemplatesRenderer(
            TEMPLATES_PATH / "root",
            self.path)
        renderer.render()

    def get_envs(self) -> dict[str, Env]:
        """List all Environments in this project."""
        p_env: Path = self.sub_paths.env
        envs = {}
        for p in p_env.iterdir():
            e = Env(p.name, p)
            envs[e.name] = e
        return envs

    def add_env(self, name: str, template: str = "py-env"):
        """Add a new environment."""
        templates_path = ENV_TEMPLATES_PATH / template
        if not templates_path.exists():
            err_msg = f"Template '{template}' is not found."
            err_msg += " Available templates: "
            err_msg += " ".join(list_env_templates())
            raise IOError(err_msg)
        env = Env(name, self.sub_paths.env)
        env.create(templates_path)

    def remove_env(self, name: str):
        """Remove a env"""
        env = Env(name, self.sub_paths.env)
        env.delete()
