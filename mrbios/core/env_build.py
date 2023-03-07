import subprocess as subp
from pathlib import Path
import os

import yaml

from ..utils.log import console
from ..utils.misc import command_exist


class EnvBuild():
    pass


class CondaEnvBuild(EnvBuild):
    def __init__(self, project_name: str, config: dict):
        self.config = config
        self.env_name = f"{project_name}-{config['name']}"
        self.conda_config = CondaConfig(
            self.env_name,
            config.get("conda", {}))
        self.pip_config = PipConfig(
            config.get("pip", {}))
        self.r_config = RConfig(
            config.get("R", {}))

    @classmethod
    def from_config_file(cls, path: str | Path) -> "CondaEnvBuild":
        with open(path) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        project_name = Path(path).parent.parent.parent.name
        build = CondaEnvBuild(project_name, config)
        return build

    def build(self):
        self.conda_config.check_install_command()
        self.conda_config.create_env()
        # Install pip packages
        if not self.pip_config.is_empty:
            self.conda_config.run_under_env(
                self.pip_config.get_install_command()
            )
        if not self.r_config.is_empty:
            self.conda_config.set_r_lib_path()
            # Install CRAN packages
            if len(self.r_config.cran_dependents) > 0:
                self.conda_config.run_under_env(
                    self.r_config.get_cran_command()
                )
            # Install Bioconductor packages
            if len(self.r_config.bioconductor_dependents) > 0:
                self.conda_config.run_under_env(
                    self.r_config.get_bioconductor_command()
                )
            # Install github packages
            if len(self.r_config.github_dependents) > 0:
                self.conda_config.run_under_env(
                    self.r_config.get_devtools_command()
                )

    def delete(self):
        self.conda_config.remove_env()


class CondaConfig():
    def __init__(self, env_name: str, config: dict):
        self.env_name = env_name
        self.config = config
        self.channels = config.get("channels", [])
        self.dependents = config.get("deps", [])
        self.install_command = self.config.get("install_command", "conda")

    def check_install_command(self):  # pragma: no cover
        if not command_exist(self.install_command):
            if self.install_command != "conda":
                console.log(
                    f"[error]{self.install_command} not installed, "
                    "turn to using conda[/error]")
                self.install_command = "conda"
                self.check_install_command()
            else:
                raise SystemError("Conda is not installed.")

    def _get_install_cmd(self, main_cmd: str) -> list[str]:
        cmd = [self.install_command, main_cmd, "-n", self.env_name]
        for c in self.channels:
            cmd.append("-c")
            cmd.append(c)
        cmd += self.dependents + ["--yes"]
        return cmd

    def _run_cmd(self, cmd: list[str], cmd_name: str):
        cmd_str = " ".join(cmd)
        console.log(f"Run command [path]{cmd_str}[/path]")
        try:
            subp.check_call(cmd, env=os.environ.copy())
        except Exception as e:
            console.log(
                f"[error]Failed to {cmd_name} env "
                f"[note]{self.env_name}[/note][error]")
            raise e

    def create_env(self):
        cmd = self._get_install_cmd("create")
        self._run_cmd(cmd, "create")

    def remove_env(self):
        cmd = [
            "conda", "env", "remove", "-n",
            self.env_name
        ]
        self._run_cmd(cmd, "remove")

    def _get_conda_run_cmd(self, command: list[str]) -> list[str]:
        """Get the command to run under conda env."""
        cmd = [
            "conda", "run", "--no-capture-output",
            "-n", self.env_name
        ]
        cmd += command
        return cmd

    def run_under_env(self, command: list[str]):
        """Run command under conda env."""
        cmd = self._get_conda_run_cmd(command)
        self._run_cmd(cmd, "run command in")

    @property
    def env_path(self) -> Path:
        """Get the path of conda env."""
        # get the output of conda env list
        cmd = ["conda", "env", "list"]
        cmd = self._get_conda_run_cmd(cmd)
        out = subp.check_output(cmd).decode()
        # find the path of env
        for line in out.splitlines():
            if "*" in line:
                env_path = line.split()[2]
                return Path(env_path)
        else:
            raise ValueError("Cannot find conda env path.")

    @property
    def is_built(self) -> bool:
        """Check if the env is built."""
        cmd = ["conda", "run", "-n", self.env_name, "conda", "--version"]
        try:
            subp.check_call(
                cmd, env=os.environ.copy(),
                stdout=subp.DEVNULL, stderr=subp.DEVNULL)
        except subp.CalledProcessError:
            return False
        return True

    def set_r_lib_path(self):
        """Set the R_LIBS_USER env variable."""
        env_path = self.env_path
        r_lib_path = env_path / "Lib/R/library"
        console.log(f"Set R_LIBS_USER to [path]{r_lib_path}[/path]")
        os.environ["R_LIBS_USER"] = str(r_lib_path)


class PipConfig():
    """Pip config for conda env build."""
    def __init__(self, config: dict):
        self.config = config

    @property
    def is_empty(self) -> bool:
        return len(self.dependents) == 0

    @property
    def dependents(self) -> list[str]:
        return self.config.get("deps", [])

    def get_install_command(self) -> list[str]:
        """Get pip install command. """
        cmd = ["pip", "install"]
        cmd += self.dependents
        return cmd


class RConfig(EnvBuild):
    """R config for conda env build."""
    def __init__(self, config: dict):
        self.config = config
        # load config for cran, bioconductor, devtools
        self.cran_config = config.get("cran", {})
        self.bioconductor_config = config.get("bioconductor", {})
        self.devtools_config = config.get("github", {})

    @property
    def is_empty(self) -> bool:
        return len(self.cran_dependents) == 0 and \
            len(self.bioconductor_dependents) == 0 and \
            len(self.github_dependents) == 0

    @property
    def cran_mirror(self) -> str:
        default_mirror = "https://cloud.r-project.org/"
        return self.cran_config.get("mirror", default_mirror)

    @property
    def cran_dependents(self) -> list[str]:
        return self.cran_config.get("deps", [])

    @property
    def bioconductor_mirror(self) -> str | None:
        return self.bioconductor_config.get("mirror")

    @property
    def bioconductor_dependents(self) -> list[str]:
        return self.bioconductor_config.get("deps", [])

    @property
    def github_dependents(self) -> list[str]:
        return self.devtools_config.get("deps", [])

    def get_cran_command(self) -> list[str]:
        """Get cran install command. """
        dependents = self.cran_dependents
        if len(dependents) > 1:
            dependents = [f"'{d}'" for d in dependents]
            pkgs_str = f"c({', '.join(dependents)})"
        else:
            pkgs_str = f"'{dependents[0]}'"
        install_inst = (
            f"install.packages({pkgs_str}, "
            f"repos='{self.cran_mirror}')"
        )
        cmd = ["Rscript", "-e", f'{install_inst}']
        return cmd

    def get_bioconductor_command(self) -> list[str]:
        """Get bioconductor install command. """
        dependents = self.bioconductor_dependents
        if len(dependents) > 1:
            dependents = [f"'{d}'" for d in dependents]
            pkgs_str = f"c({', '.join(dependents)})"
        else:
            pkgs_str = f"'{dependents[0]}'"
        install_inst = (
            "if (!requireNamespace('BiocManager', quietly = TRUE)) "
            f"install.packages('BiocManager', repos='{self.cran_mirror}'); "
            f"BiocManager::install({pkgs_str})"
        )
        if self.bioconductor_mirror is not None:  # pragma: no cover
            install_inst = (
                f"options(BioC_mirror='{self.bioconductor_mirror}'); " +
                install_inst
            )
        cmd = ["Rscript", "-e", f'{install_inst}']
        return cmd

    def get_devtools_command(self) -> list[str]:
        """Get devtools install command. """
        dependents = self.github_dependents
        if len(dependents) > 1:
            dependents = [f"'{d}'" for d in dependents]
            pkgs_str = f"c({', '.join(dependents)})"
        else:
            pkgs_str = f"'{dependents[0]}'"
        install_inst = (
            "if (!requireNamespace('devtools', quietly = TRUE)) "
            f"install.packages('devtools', repos='{self.cran_mirror}'); "
            f"devtools::install_github({pkgs_str})"
        )
        cmd = ["Rscript", "-e", f'{install_inst}']
        return cmd
