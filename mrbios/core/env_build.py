import subprocess as subp
from pathlib import Path

import yaml

from ..utils.log import console
from ..utils.misc import command_exist


class EnvBuild():
    pass


class CondaEnvBuild(EnvBuild):
    def __init__(self, config: dict):
        self.config = config
        self.env_name = config['name']
        self.conda_config = CondaConfig(
            self.env_name,
            config.get("conda", {}))
        self.pip_config = PipConfig(
            config.get("pip", {}))

    @classmethod
    def from_config_file(cls, path: str | Path) -> "CondaEnvBuild":
        with open(path) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        build = CondaEnvBuild(config)
        return build

    def build(self):
        self.conda_config.check_command()
        self.conda_config.create_env()

    def delete(self):
        self.conda_config.remove_env()


class CondaConfig():
    def __init__(self, env_name: str, config: dict):
        self.env_name = env_name
        self.config = config
        self.channels = config.get("channels", [])
        self.dependents = config.get("deps", [])
        self.command = self.config.get("command", "conda")

    def check_command(self):
        if not command_exist(self.command):
            if self.command != "conda":
                console.log(
                    f"[error]{self.command} not installed, "
                    "turn to using conda[/error]")
                self.command = "conda"
                self.check_command()
            else:
                raise SystemError("Conda is not installed.")

    def _get_cmd(self, main_cmd: str) -> list[str]:
        cmd = [self.command, main_cmd, "-n", self.env_name]
        for c in self.channels:
            cmd.append("-c")
            cmd.append(c)
        cmd += self.dependents + ["--yes"]
        return cmd

    def _run_cmd(self, cmd: list[str], cmd_name: str):
        cmd_str = " ".join(cmd)
        console.log(f"Run command '[note]{cmd_str}[/note]'")
        try:
            subp.check_call(cmd)
        except Exception as e:
            console.log(
                f"[error]Failed to {cmd_name} env {self.env_name}[error]")
            raise e

    def create_env(self):
        cmd = self._get_cmd("create")
        self._run_cmd(cmd, "create")

    def install_dependents(self):
        cmd = self._get_cmd("install")
        self._run_cmd(cmd, "install")

    def remove_env(self):
        cmd = [
            self.command, "env", "remove", "-n",
            self.env_name
        ]
        self._run_cmd(cmd, "remove")


class PipConfig():
    def __init__(self, config: dict):
        self.config = config

    @property
    def dependents(self) -> list[str]:
        return self.config.get("deps", [])
