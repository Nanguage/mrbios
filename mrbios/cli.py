import sys
import shlex
import os.path
from pathlib import Path

from .core.project import Project
from .core.platform import Platform
from .core.dir_obj import Env, Script
from .utils.template import list_env_templates, list_script_templates
from .utils.log import console, Confirm, Prompt
from .utils.user_setting import UserSetting, DEFAULT_SETTING_PATH


class SubCLI():
    def __init__(self, parent: "CLI"):
        self._parent = parent
        self._proj = parent._proj


class ProjectManager(SubCLI):
    """Tools for manage the project structure."""

    def create(self, path: str):
        """Create a project to specific path."""
        proj = Project(path)
        proj.create()
        self._parent.set_current_project(path)

    def add_env(self, name: str, template: str | None = None):
        """Add an environment to the project.

        :param name: Name of the env.
        :param template: Template of the env.
        Using `list_env_templates` to see all
        available env templates.
        """
        if template is None:
            templates = list_env_templates()
            template = Prompt.ask(
                "Choice a template",
                choices=templates,
                default=templates[0])
        self._proj.add_env(name, template)

    def remove_env(self, name: str):
        """Remove an environment."""
        is_remove = Confirm.ask(
            f"Do you want to remove env: [note]{name}[/note]?")
        if is_remove:
            self._proj.remove_env(name)

    def list_envs(self):
        """List all existing envs."""
        msg = "Existing envs:\n"
        for env in self._proj.get_envs().values():
            msg += repr(env) + "\n"
        console.print(msg)

    def list_env_templates(self):
        """List all available env templates."""
        console.log("Available env templates:")
        console.print(list_env_templates())

    def add_file_type(
            self, name: str,
            description: str | None = None,
            ):
        """Add a file type"""
        if description is None:
            description = Prompt.ask(
                "[blue]Give a short description about the file type[/blue]"
            )
        self._proj.add_file_type(name, description)

    def remove_file_type(self, name: str):
        """Remove a file type."""
        is_remove = Confirm.ask(
            f"Do you want to remove file type: [note]{name}[/note]?")
        if is_remove:
            self._proj.remove_file_type(name)

    def list_file_types(self):
        """List all existing file types."""
        msg = "Existing file types:\n"
        for ft in self._proj.get_file_types().values():
            msg += repr(ft) + "\n"
        console.print(msg)

    def add_file_format(
            self, name,
            file_type: str | None = None,
            description: str | None = None):
        """Add a file format"""
        if file_type is None:
            file_types = [
                ft.name for ft in
                self._proj.get_file_types().values()
            ]
            file_type = Prompt.ask(
                "Select a file type",
                choices=file_types,
            )
        if description is None:
            description = Prompt.ask(
                "[blue]Give a short description about the file format[/blue]"
            )
        self._proj.add_file_format(file_type, name, description)

    def remove_file_format(self, file_type: str, name: str):
        """Remove a file format."""
        is_remove = Confirm.ask(
            "Do you want to remove file format: "
            f"[note]{file_type}/{name}[/note]?")
        if is_remove:
            self._proj.remove_file_format(file_type, name)

    def list_file_formats(self, file_type: str = "All"):
        """List file formats.

        :param file_type: Specify file_type, if not set will list all.
        """
        if file_type.lower() == "all":
            info = self._proj.get_all_file_formats()
            for ft_name, formats in info.items():
                console.print(f"[note]{ft_name}[/note]:")
                fm_names = " ".join([f for f in formats.keys()])
                console.print(fm_names)
                console.print()
        else:
            formats = self._proj.get_file_formats(file_type)
            fm_names = " ".join([f for f in formats.keys()])
            console.print(fm_names)

    def add_task(self, name: str, description: str | None = None):
        """Add a task."""
        if description is None:
            description = Prompt.ask(
                "[blue]Give a short description about the task[/blue]"
            )
        self._proj.add_task(name, description)

    def remove_task(self, name: str):
        """Remove a task."""
        is_remove = Confirm.ask(
            f"Do you want to remove task: [note]{name}[/note]?")
        if is_remove:
            self._proj.remove_task(name)

    def list_tasks(self):
        """List all existing tasks."""
        msg = "Existing tasks:\n"
        for task in self._proj.get_tasks().values():
            msg += repr(task) + "\n"
        console.print(msg)

    def add_script(
            self, name: str,
            task: str | None = None,
            template: str | None = None,
            description: str | None = None):
        """Add a script."""
        if task is None:
            tasks = [
                t.name for t in
                self._proj.get_tasks().values()
            ]
            task = Prompt.ask(
                "Select a task",
                choices=tasks,
            )
        if template is None:
            template = Prompt.ask(
                "Select a script template",
                choices=list_script_templates(),
            )
        if description is None:
            description = Prompt.ask(
                "[blue]Give a short description about the script[/blue]"
            )
        self._proj.add_script(task, name, template, description)

    def remove_script(self, task: str, name: str):
        """Remove a script."""
        is_remove = Confirm.ask(
            "Do you want to remove script: "
            f"[note]{task}/{name}[/note]?")
        if is_remove:
            self._proj.remove_script(task, name)

    def list_scripts(self, task: str = "All"):
        """List scripts.

        :param task: Specify task, if not set will list all.
        """
        if task.lower() == "all":
            info = self._proj.get_all_scripts()
            for task_name, scripts in info.items():
                console.print(f"[note]{task_name}[/note]:")
                script_names = " ".join([f for f in scripts.keys()])
                console.print(script_names)
                console.print()
        else:
            scripts = self._proj.get_scripts(task)
            script_names = " ".join([f for f in scripts.keys()])
            console.print(script_names)


class EnvBuild(SubCLI):
    """Tools for manage environments build."""
    def _select_env(
            self, env_name: str | None = None
            ) -> tuple[str, Env] | None:
        envs = self._proj.get_envs()
        if len(envs) == 0:
            console.log("No existing envs for build.")
            return None
        if env_name is None:
            env_name = Prompt.ask(
                "Select a env",
                choices=list(envs.keys()))
        env = envs[env_name]
        return env_name, env

    list = ProjectManager.list_envs

    def build(self, env_name: str | None = None):
        """Build an env."""
        name_and_env = self._select_env(env_name)
        if name_and_env is not None:
            env_name, env = name_and_env
            console.log(f"Start building [note]{env_name}[/note]")
            env.build()
            console.log(
                f"The env [note]{env_name}[/note] "
                "has aleardy been built.")

    def build_all(self, force: bool = False):
        """Build all unbuilt envs.

        :param force: Force to build all envs.
        """
        envs = self._proj.get_envs()
        for name, env in envs.items():
            if (not env.is_built) or force:
                console.log(
                    f"Start building [note]{name}[/note]")
                env.build()
                console.log(
                    f"The env [note]{name}[/note] has aleardy been built.")

    def update(self, env_name: str | None = None):
        """Update a built env."""
        name_and_env = self._select_env(env_name)
        if name_and_env is not None:
            env_name, env = name_and_env
            console.log(f"Start updating [note]{env_name}[/note]")
            env.update()
            console.log(
                f"The env [note]{env_name}[/note] has aleardy been updated.")

    def update_all(self):
        """Update all built envs."""
        envs = self._proj.get_envs()
        for name, env in envs.items():
            if env.is_built:
                console.log(
                    f"Start updating [note]{name}[/note]")
                env.update()
                console.log(
                    f"The env [note]{name}[/note] has aleardy been updated.")

    def delete(self, env_name: str | None = None):
        """Delete a built env."""
        name_and_env = self._select_env(env_name)
        if name_and_env is not None:
            env_name, env = name_and_env
            remove = Confirm.ask(
                "Do you want to remove the env "
                f"[note]{env_name}[/note]?")
            if remove:
                env.delete_built()
                console.log(
                    f"The env [note]{env_name}[/note] "
                    "has aleardy been removed.")

    def clear_all(self):
        """Delete all built env."""
        envs = self._proj.get_envs()
        for name, env in envs.items():
            if env.is_built:
                env.delete_built()
                console.log(
                    f"The env [note]{name}[/note] has aleardy been removed.")

    def rebuild(self, env_name: str | None = None):
        """Rebuild a built env."""
        name_and_env = self._select_env(env_name)
        if name_and_env is not None:
            env_name, env = name_and_env
            if env.is_built:
                env.delete_built()
                console.log(
                    f"The env [note]{env_name}[/note] "
                    "has aleardy been removed.")
            console.log(f"Start building [note]{env_name}[/note]")
            env.build()
            console.log(
                f"The env [note]{env_name}[/note] "
                "has aleardy been built.")

    def rebuild_all(self):
        """Rebuild all built envs."""
        envs = self._proj.get_envs()
        for name, env in envs.items():
            if env.is_built:
                env.delete_built()
                console.log(
                    f"The env [note]{name}[/note] has aleardy been removed.")
                console.log(f"Start building [note]{name}[/note]")
                env.build()
                console.log(
                    f"The env [note]{name}[/note] has aleardy been built.")

    def run(self, command: str, env_name: str | None = None):
        """Run command under an env."""
        name_and_env = self._select_env(env_name)
        if name_and_env:
            env_name, env = name_and_env
            if not env.is_built:
                console.log(
                    f"[error]The env [blue]{env_name}[/blue] not "
                    "yet built. Please build it first.[/error]")
                sys.exit(1)
            cmd = shlex.split(command)
            console.log(
                f"Run command [path]{command}[/path] under "
                f"env [note]{env_name}[/note].")
            env.run_command(cmd)
            console.log(
                f"The command has been successfully "
                f"run under env [note]{env_name}[/note].")


class ScriptRun(SubCLI):
    """Tools for running scripts."""

    def _get_script(self, task_script: str) -> tuple[str, Script]:
        task, script = task_script.split("/")
        scripts = self._proj.get_scripts(task)
        if script in scripts:
            return task, scripts[script]
        else:
            console.log(
                f"[error]The script [blue]{script}[/blue] "
                f"not found under task [blue]{task}[/blue].[/error]")
            sys.exit(1)

    def run(self, task_script: str, *args, **kwargs):
        """Run a script.

        :param task_script: The task and script name, separated by a '/',
        like "task1/script1".
        """
        task_name, script = self._get_script(task_script)
        console.log(
            f"Run script [note]{script.name}[/note] under task "
            f"[note]{task_name}[/note].")
        script.runner.run(*args, **kwargs)
        console.log(
            f"The script [note]{script.name}[/note] has been "
            f"successfully run under task [note]{task_name}[/note].")

    def qt_gui(self, task_script: str):  # pragma: no cover
        """Run a script with Qt GUI.

        :param task_script: The task and script name, separated by a '/',
        like "task1/script1".
        """
        task_name, script = self._get_script(task_script)
        console.log(
            f"Run script [note]{script.name}[/note] under task "
            f"[note]{task_name}[/note] with Qt GUI.")
        script.runner.run_with_qt_gui()
        console.log(
            f"The script [note]{script.name}[/note] has been "
            f"successfully run under task [note]{task_name}[/note] "
            "with Qt GUI.")

    def dash_app(self, task_script: str):  # pragma: no cover
        """Run a script with Dash App.

        :param task_script: The task and script name, separated by a '/',
        like "task1/script1".
        """
        task_name, script = self._get_script(task_script)
        console.log(
            f"Run script [note]{script.name}[/note] under task "
            f"[note]{task_name}[/note] with Dash App.")
        script.runner.run_with_dash_app()
        console.log(
            f"The script [note]{script.name}[/note] has been "
            f"successfully run under task [note]{task_name}[/note] "
            "with Dash App.")


class PlatformLauncher(SubCLI):
    """Tools for launching the executor platform server."""

    def run_server(self):  # pragma: no cover
        """Run the executor platform server."""
        platform = Platform(self._proj.path)
        platform.run_server()


class CLI():
    def __init__(
            self,
            user_setting_path: str = str(DEFAULT_SETTING_PATH),
            ):
        self._user_setting = UserSetting(Path(user_setting_path))
        console.log(
            f"Using user setting: [note]{user_setting_path}[/note]")
        path = self._user_setting.attrs.get("project_path", "./")
        self._proj = Project(path)
        self.print_current_project()
        # command groups
        self.project = ProjectManager(self)
        self.env = EnvBuild(self)
        self.script = ScriptRun(self)
        self.platform = PlatformLauncher(self)

    def print_current_project(self):
        """Print the current project path."""
        console.log(
            "Current project: "
            f"[path]{self._proj.path}[/path]")

    def set_current_project(self, path: str):
        """Set working project path."""
        path = os.path.abspath(path)
        self._user_setting.update({"project_path": path})
        self._proj = Project(path)
        console.log(
            "Set working project path "
            f"to [path]{path}[/path]")


if __name__ == "__main__":
    import fire
    fire.Fire(CLI)
