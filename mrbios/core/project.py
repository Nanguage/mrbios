import typing as T
from pathlib import Path
import json
from datetime import datetime

from ..utils.log import console
from ..utils.template import (
    TemplatesRenderer, ENV_TEMPLATES_PATH,
    TEMPLATES_PATH, list_env_templates,
    FILE_TYPE_TEMPLATE_PATH,
    FILE_FORMAT_TEMPLATE_PATH,
    TASK_TEMPLATE_PATH,
    SCRIPT_TEMPLATE_PATH,
    list_script_templates,
)
from .dir_obj import (
    DirObj, Env,
    FileType, FileFormat,
    Task, Script,
)


class SubPaths(T.NamedTuple):
    """Project's sub-paths."""
    env: Path
    task: Path
    pipe: Path
    format: Path


def path_is_project(path: Path) -> bool:
    """Check if the path is a project."""
    if not (path / ".meta.json").exists():
        return False
    else:
        flag = False
        with open(path / ".meta.json") as f:
            info = json.load(f)
            if "mrbios-version" in info:
                flag = True
        return flag


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

    @property
    def is_exist(self) -> bool:
        """Check if the project exists."""
        return self.path.exists()

    def check_exist(self):
        """Check if the project exists."""
        if not self.is_exist:
            raise IOError(
                f"Project '{self.name}({self.path})' is not exist."
                " Please create it first.")

    @property
    def meta_info(self) -> dict:
        """Get the meta info of the project."""
        self.check_exist()
        meta_file = self.path / ".meta.json"
        if not meta_file.exists():  # pragma: no cover
            return {}
        with open(meta_file) as f:
            return json.load(f)

    @meta_info.setter
    def meta_info(self, value: dict):
        """Set the meta info of the project."""
        self.check_exist()
        meta_file = self.path / ".meta.json"
        with open(meta_file, 'w') as f:
            json.dump(value, f, indent=4)

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
        # init meta info
        from .. import __version__
        self.meta_info = {
            "mrbios-version": __version__,
            "created-time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
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
        self.check_exist()
        return self._get_dirobjs(self.sub_paths.env, Env)

    def add_env(self, name: str, template: str = "py-env"):
        """Add a new environment."""
        self.check_exist()
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
        self.check_exist()
        env = Env(name, self.sub_paths.env)
        env.delete()

    def get_file_types(self) -> dict[str, FileType]:
        """Get all file types"""
        self.check_exist()
        return self._get_dirobjs(self.sub_paths.format, FileType)

    def add_file_type(self, name: str, description: str):
        """Add a new file type."""
        self.check_exist()
        file_type = FileType(name, self.sub_paths.format)
        file_type.create(
            FILE_TYPE_TEMPLATE_PATH,
            description=description,
        )

    def remove_file_type(self, name: str):
        """Remove a file type."""
        self.check_exist()
        file_type = FileType(name, self.sub_paths.format)
        file_type.delete()

    def add_file_format(
            self, file_type: str, name: str,
            description: str):
        """Add a new file format"""
        self.check_exist()
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
        self.check_exist()
        type_path = self.sub_paths.format / file_type
        if not type_path.exists():
            raise IOError(
                f"File type {file_type} is not exist.")
        file_format = FileFormat(name, type_path)
        file_format.delete()

    def get_file_formats(self, file_type: str) -> dict[str, FileFormat]:
        """Get file formats in specific file type."""
        self.check_exist()
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
        self.check_exist()
        info = {}
        for path in self.sub_paths.format.iterdir():
            if path.is_dir():
                formats = self.get_file_formats(path.name)
                info[path.name] = formats
        return info

    def add_task(self, name: str, description: str):
        """Add a new task."""
        self.check_exist()
        task = Task(name, self.sub_paths.task)
        task.create(
            TASK_TEMPLATE_PATH,
            description=description,
        )

    def remove_task(self, name):
        """Remove a task."""
        self.check_exist()
        task = Task(name, self.sub_paths.task)
        task.delete()

    def get_tasks(self) -> dict[str, Task]:
        """Get all tasks."""
        self.check_exist()
        return self._get_dirobjs(self.sub_paths.task, Task)

    def add_script(
            self, task: str, name: str,
            template: str,
            description: str):
        """Add a new script."""
        self.check_exist()
        task_path = self.sub_paths.task / task
        if not task_path.exists():
            raise IOError(
                f"Task {task} is not exist.")

        templates_path = SCRIPT_TEMPLATE_PATH / template
        if not templates_path.exists():
            err_msg = f"Template '{template}' is not found."
            err_msg += " Available templates: "
            err_msg += " ".join(list_script_templates())
            raise IOError(err_msg)

        script = Script(name, task_path)
        script.create(
            templates_path,
            description=description
        )

    def remove_script(self, task: str, name: str):
        """Remove a script."""
        self.check_exist()
        task_path = self.sub_paths.task / task
        if not task_path.exists():
            raise IOError(
                f"Task {task} is not exist.")
        script = Script(name, task_path)
        script.delete()

    def get_scripts(self, task: str) -> dict[str, Script]:
        """Get scripts in specific task."""
        self.check_exist()
        task_path = self.sub_paths.task / task
        if not task_path.exists():
            raise IOError(
                f"Task {task} is not exist.")
        task_obj = Task(task, self.sub_paths.task)
        scripts = {
            s.name: s for s in task_obj.scripts
        }
        return scripts

    def get_all_scripts(self) -> dict[str, dict[str, Script]]:
        """Get all scripts."""
        self.check_exist()
        info = {}
        for path in self.sub_paths.task.iterdir():
            if path.is_dir():
                scripts = self.get_scripts(path.name)
                info[path.name] = scripts
        return info
