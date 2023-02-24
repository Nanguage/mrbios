import typing as T
from pathlib import Path

from .utils.log import console
from .utils.misc import TemplatesRenderer


TEMPLATES_PATH = Path(__file__).parent / "templates"


def list_env_templates() -> list[str]:
    env_templates_path = TEMPLATES_PATH / "envs"
    return [
        str(i.name) for i in env_templates_path.glob("*")
    ]


class Env():
    def __init__(self, name: str, base_path: Path):
        self.name = name
        self.base_path = base_path
        self.path = self.base_path / name

    def create(self,  templates_path: Path):
        """Create the Environment."""
        renderer = TemplatesRenderer(templates_path, self.path)
        if not self.is_exist:
            console.log(f"Creating env: [note]'{self.name}'[note]")
            self.path.mkdir(parents=True)
            renderer.render(name=self.name)
            console.log(f"{repr(self)}")
        else:
            console.log(
                f"{self.name} aleardy exist at [path]{self.path}[/path]")

    @property
    def is_exist(self) -> bool:
        return self.path.exists()

    def __repr__(self):
        e = "created" if self.is_exist else "uncreated"
        return f"Env at [path]{self.path}[/path] ({e})"


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

    def list_envs(self) -> list[Env]:
        """List all Environments in this project."""
        p_env: Path = self.sub_paths.env
        envs = []
        for p in p_env.iterdir():
            e = Env(p.name, p)
            envs.append(e)
        return envs

    def add_env(self, name: str, template: str = "py-env"):
        """Add a new environment."""
        templates_path = TEMPLATES_PATH / "envs" / template
        if not templates_path.exists():
            err_msg = f"Template '{template}' is not found."
            err_msg += " Available templates: "
            err_msg += " ".join(list_env_templates())
            raise IOError(err_msg)
        env = Env(name, self.sub_paths.env)
        env.create(templates_path)
