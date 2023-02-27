import typing as T
from pathlib import Path

from ..utils.log import console
from ..utils.misc import (
    TemplatesRenderer, ENV_TEMPLATES_PATH,
    TEMPLATES_PATH, list_env_templates,
    FILE_TYPE_TEMPLATE_PATH,
    FILE_FORMAT_TEMPLATE_PATH,
)
from .dir_obj import DirObj
from .env import Env
from .file_type import FileType
from .file_format import FileFormat


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

    def _get_dirobjs(
            self, path: Path,
            cls: T.Type[DirObj],
            ) -> dict:
        objs = {}
        for p in path.iterdir():
            e = cls(p.name, path)
            objs[e.name] = e
        return objs

    def get_envs(self) -> dict[str, Env]:
        """Get all environments in this project."""
        return self._get_dirobjs(self.sub_paths.env, Env)

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
        """Remove a env."""
        env = Env(name, self.sub_paths.env)
        env.delete()

    def get_file_types(self) -> dict[str, FileType]:
        """Get all file types"""
        return self._get_dirobjs(self.sub_paths.format, FileType)

    def add_file_type(self, name: str, description: str):
        """Add a new file type."""
        file_type = FileType(name, self.sub_paths.format)
        file_type.create(
            FILE_TYPE_TEMPLATE_PATH,
            description=description,
        )

    def remove_file_type(self, name: str):
        """Remove a file type."""
        file_type = FileType(name, self.sub_paths.format)
        file_type.delete()

    def add_file_format(
            self, file_type: str, name: str,
            description: str):
        """Add a new file format"""
        type_path = self.sub_paths.format / file_type
        if not type_path.exists():
            raise IOError(
                f"File type {file_type} is not exist.")
        file_format = FileFormat(name, type_path)
        file_format.create(
            FILE_FORMAT_TEMPLATE_PATH,
            description=description
        )

    def remove_file_format(self, file_type: str, name: str):
        """Remove a file format"""
        type_path = self.sub_paths.format / file_type
        if not type_path.exists():
            raise IOError(
                f"File type {file_type} is not exist.")
        file_format = FileFormat(name, type_path)
        file_format.delete()

    def get_file_formats(self, file_type: str) -> dict[str, FileFormat]:
        """Get file formats in specific file type."""
        type_path = self.sub_paths.format / file_type
        if not type_path.exists():
            raise IOError(
                f"File type {file_type} is not exist.")
        ft = FileType(file_type, self.sub_paths.format)
        formats = {
            fm.name: fm for fm in ft.file_formats
        }
        return formats

    def get_all_file_formats(self) -> dict[str, dict[str, FileFormat]]:
        """Get all file formats."""
        info = {}
        for path in self.sub_paths.format.iterdir():
            if path.is_dir():
                formats = self.get_file_formats(path.name)
                info[path.name] = formats
        return info
