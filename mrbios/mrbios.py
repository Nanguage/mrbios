import typing as T
from pathlib import Path

from loguru import logger


class TemplatesRenderer():
    """For render all templates from source dir to target dir."""
    def __init__(self, templates_path: Path, target_path: Path):
        self.templates_path = templates_path
        self.target_path = target_path

    def render(self, **kwargs):
        """Render and save to target path.
        
        Provide variables by **kwargs.
        """
        logger.info(f"Render templates at {self.templates_path} to {self.target_path}")


class Env():
    def __init__(self, name: str, base_path: Path, templates_path: Path):
        self.name = name
        self.base_path = base_path
        self.path = self.base_path / name
        self.renderer = TemplatesRenderer(templates_path, self.path)

    def create(self):
        """Create the Environment."""
        if not self.is_exist:
            logger.info("Creating env {name}...")
            self.path.mkdir(parents=True)
            self.renderer.render(name=self.name)
            logger.info(f"{repr(self)}")
        else:
            logger.info(f"{self.name} aleardy exist at {self.path}")

    @property
    def is_exist(self) -> bool:
        return self.path.exists()

    def __repr__(self):
        e = "created" if self.is_exist else "uncreated"
        return f"Env at {self.path}, ({e})"


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
        p = self.path
        if not p.exists():
            p.mkdir(parents=True)
        for sub in self.sub_paths:
            if not sub.exists():
                sub.mkdir(parents=True)

    def list_envs(self) -> list[Env]:
        """List all Environments in this project."""
        p_env: Path = self.sub_paths.env
        envs = []
        for p in p_env.iterdir():
            e = Env(p.name)
            envs.append(e)
        return envs

    def add_env(self, name: str):
        """Add a new environment."""
        env = Env(name, self.sub_paths.env)
        env.create()


class MrBios():
    """The interface of Mr.BIOS."""
    def __init__(self, path="./"):
        self.proj = Project(path)

    def add_env(self, name: str):
        self.proj.add_env(name)
        return self

    def create_project(self, path: str):
        proj = Project(path)
        proj.create()
        self.proj = proj
        return self

