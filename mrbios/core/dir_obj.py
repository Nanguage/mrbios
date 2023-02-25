from pathlib import Path
import shutil

from ..utils.log import console
from ..utils.misc import TemplatesRenderer


class DirObj():
    def __init__(self, name: str, base_path: Path):
        self.name = name
        self.base_path = base_path
        self.path = self.base_path / name

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

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
