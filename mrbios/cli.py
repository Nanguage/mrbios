from .core.project import Project
from .utils.misc import list_env_templates
from .utils.log import console, Confirm, Prompt


class ProjectManager():
    """Tools for manage the project structure."""
    def __init__(self, path="./"):
        self._proj = Project(path)

    def set_path(self, path="./"):
        """Set current project path(default './')."""
        self._proj = Project(path)
        return self

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

    def create(self, path: str):
        """Create a project to specific path."""
        proj = Project(path)
        proj.create()
        self._proj = proj

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


class CLI():
    def __init__(self):
        # command groups
        self.project = ProjectManager()


if __name__ == "__main__":
    import fire
    fire.Fire(CLI)
