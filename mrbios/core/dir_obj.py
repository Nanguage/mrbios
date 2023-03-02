from pathlib import Path
import shutil
import json
from datetime import datetime

from ..utils.log import console
from ..utils.template import TemplatesRenderer
from .env_build import CondaEnvBuild


class DirObj():
    def __init__(self, name: str, base_path: Path):
        self.name = name
        self.base_path = base_path
        self.path = self.base_path / name
        self._meta_store_file = '.meta.json'

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    @property
    def meta_info_path(self) -> Path:
        return self.path / self._meta_store_file

    @property
    def meta_info(self) -> dict:
        with open(self.meta_info_path) as f:
            info = json.load(f)
        return info

    @meta_info.setter
    def meta_info(self, value: dict):
        with open(self.meta_info_path, 'w') as f:
            json.dump(value, f, indent=4)

    def create(self, templates_path: Path, **kwargs):
        renderer = TemplatesRenderer(templates_path, self.path)
        if not self.is_exist:
            console.log(
                f"Creating {self.class_name.lower()}: "
                f"[note]'{self.name}'[note]")
            self.path.mkdir(parents=True)
            params = {"name": self.name}
            params.update(kwargs)
            renderer.render(**params)
            self.meta_info = kwargs
            console.log(f"{repr(self)}")
        else:
            console.log(
                f"[note]{self.name}[/note] aleardy exist "
                f"at [path]{self.path}[/path]")

    def delete(self):
        if self.path.exists():
            console.log(
                f"Remove {self.class_name.lower()} at "
                f"[path]{self.path.absolute()}[/path]")
            shutil.rmtree(self.path)
        else:
            err_msg = f"{self} is not exist."
            console.log(f"[error]{err_msg}[/error]")
            raise IOError(err_msg)

    @property
    def is_exist(self) -> bool:
        return self.path.exists()

    def __repr__(self):
        e = "created" if self.is_exist else "uncreated"
        return f"{self.class_name} at [path]{self.path}[/path] ({e})"


class Env(DirObj):
    @property
    def build_config(self) -> CondaEnvBuild:
        return CondaEnvBuild.from_config_file(self.path / "build.yaml")

    def build(self):
        self.build_config.build()
        new_info = self.meta_info.copy()
        new_info['build-time'] = str(datetime.now())
        self.meta_info = new_info

    def delete_built(self):
        """Delete the built conda env."""
        self.build_config.delete()
        new_info = self.meta_info.copy()
        new_info['build-time'] = None
        self.meta_info = new_info

    @property
    def is_built(self) -> bool:
        if self.meta_info.get("build-time") is None:
            return False
        else:
            return True

    def run_command(self, command: list[str]):
        """Run command under the built env.

        :param command: The command need to run.
        """
        self.build_config.conda_config.run_under_env(command)

    def __repr__(self):
        e = "created" if self.is_exist else "uncreated"
        if self.is_built:
            build_msg = "[note]built[/note]"
        else:
            build_msg = "[error]unbuilt[/error]"
        msg = (
            f"{self.class_name} at [path]{self.path}[/path] "
            f"({e}, {build_msg})"
        )
        return msg


class FileType(DirObj):
    @property
    def file_formats(self) -> list["FileFormat"]:
        formats = []
        for p in self.path.iterdir():
            if not p.is_dir():
                continue
            ff = FileFormat(p.name, self.path)
            formats.append(ff)
        return formats


class FileFormat(DirObj):
    @property
    def file_type(self) -> FileType:
        parent = self.path.parent
        return FileType(parent.name, parent.parent)


class Task(DirObj):
    @property
    def scripts(self) -> list["Script"]:
        res = []
        for p in self.path.iterdir():
            if not p.is_dir():
                continue
            s = Script(p.name, self.path)
            res.append(s)
        return res


class Script(DirObj):
    @property
    def task(self) -> Task:
        parent = self.path.parent
        return Task(parent.name, parent.parent)
