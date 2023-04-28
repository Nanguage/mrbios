from pathlib import Path
import shutil

import jinja2

from .log import console


TEMPLATES_PATH = Path(__file__).parent.parent / "templates"
ENV_TEMPLATES_PATH = TEMPLATES_PATH / "envs"
FILE_TYPE_TEMPLATE_PATH = TEMPLATES_PATH / "file_type"
FILE_FORMAT_TEMPLATE_PATH = TEMPLATES_PATH / "file_format"
TASK_TEMPLATE_PATH = TEMPLATES_PATH / "task"
SCRIPT_TEMPLATE_PATH = TEMPLATES_PATH / "script"


def list_env_templates() -> list[str]:
    return [
        str(i.name) for i in ENV_TEMPLATES_PATH.glob("*")
    ]


def list_script_templates() -> list[str]:
    return [
        str(i.name) for i in SCRIPT_TEMPLATE_PATH.glob("*")
    ]


class TemplatesRenderer():
    """For render all templates from source dir to target dir."""
    def __init__(self, templates_path: Path, target_path: Path):
        self.templates_path = templates_path
        self.target_path = target_path

    def render(self, **kwargs):
        """Render and save to target path.

        Provide variables by **kwargs.
        """
        with console.status(
                "Render templates at "
                f"[path]{self.templates_path}[/path] to "
                f"[path]{self.target_path}[/path]"):
            for path in self.templates_path.glob("*"):
                if path.name in ["__pycache__", ".DS_Store"]:
                    continue
                elif path.is_dir():
                    continue
                elif path.name.endswith(".temp"):
                    # render file
                    target = self.target_path / path.name.removesuffix(".temp")
                    console.log(
                        f"Render template [path]{path}[/path] to "
                        f"[path]{target}[/path]")
                    with open(path) as f:
                        temp_str = f.read()
                    temp = jinja2.Template(temp_str)
                    content = temp.render(**kwargs)
                    with open(target, 'w') as fo:
                        fo.write(content)
                else:
                    # copy file
                    target = self.target_path / path.name
                    console.log(f"Copy [path]{path}[/path] "
                                f"to [path]{target}[/path]")
                    shutil.copy(path, target)
