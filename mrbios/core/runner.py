import typing as T
from pathlib import Path
import shlex

import yaml
from cmd2func import cmd2func
import oneface
from funcdesc import mark_input
from funcdesc.desc import NotDef


if T.TYPE_CHECKING:
    from .project import Project


class ScriptRunner:
    def __init__(self, config: dict, base_path: str | Path):
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
        return self.env.run_command(shlex.split(cmd_str))

    def _get_run_func(self) -> T.Callable:  # pragma: no cover
        cmd_obj = cmd2func(self.command_template, self.config)

        def run(*args, **kwargs) -> int:
            cmd_str = cmd_obj.get_cmd_str(*args, **kwargs)
            return self.env.run_command(shlex.split(cmd_str))
        run.__signature__ = cmd_obj.__signature__
        for name, arg in self.config['inputs'].items():
            mark_ = mark_input(
                name,
                type=eval(arg.get('type', 'str')),
                range=arg.get('range'),
                default=arg.get('default', NotDef),
            )
            run = mark_(run)
        return run

    def run_with_qt_gui(self) -> int:  # pragma: no cover
        """Launch a Qt GUI to run the script."""
        run = self._get_run_func()
        of = oneface.one(run)
        ret_code = of.qt_gui(**self.config.get("qt_gui", {}))
        return ret_code

    def run_with_dash_app(self) -> int:  # pragma: no cover
        """Launch a Dash app to run the script."""
        run = self._get_run_func()
        of = oneface.one(run)
        ret_code = of.dash_app(**self.config.get("dash_app", {}))
        return ret_code

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
        path = Path(path)
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
        return ScriptRunner(config, path.parent)
