import typing as T
from pathlib import Path
import shlex

import yaml
from cmd2func import cmd2func


if T.TYPE_CHECKING:
    from .project import Project


class ScriptRunner:
    def __init__(self, config: dict, base_path: str | Path):
        if isinstance(base_path, str):
            base_path = Path(base_path)
        self.path = base_path
        self.config = config
        env_name = config["env"]
        self.env = self.project.get_envs()[env_name]

    @property
    def command_template(self) -> str:
        temp = self.config["command"]
        # replace local files to absolute path
        local_files = self.get_local_files()
        temp_list = shlex.split(temp)
        for i, v in enumerate(temp_list):
            if v in local_files:
                p = self.path.absolute() / v
                temp_list[i] = p.as_posix()
        temp = " ".join(temp_list)
        return temp

    def run(self, *args, **kwargs) -> int:
        cmd_obj = cmd2func(self.command_template, self.config)
        cmd_str = cmd_obj.get_cmd_str(*args, **kwargs)
        self.env.run_command(shlex.split(cmd_str))

    def get_local_files(self) -> list[str]:
        """Get the local files in the script folder."""
        it = self.path.glob("*")
        files = [p.name for p in it if p.is_file()]
        # exclude interface.yaml and README.md
        exclude_list = ["interface.yaml", "README.md"]
        files = [f for f in files if f not in exclude_list]
        return files

    @property
    def project(self) -> "Project":
        from .project import Project
        return Project(self.path.parent.parent.parent)

    @staticmethod
    def from_config_file(path: str | Path) -> "ScriptRunner":
        if isinstance(path, str):
            path = Path(path)
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
        return ScriptRunner(config, path.parent)
