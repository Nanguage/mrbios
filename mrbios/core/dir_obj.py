from pathlib import Path
import shutil
import json

from ..utils.log import console
from ..utils.misc import TemplatesRenderer


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
