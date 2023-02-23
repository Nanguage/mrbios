from .project import Project, list_env_templates
from .utils.log import logger


class ProjectManager():
    """Tools for manage the project structure."""
    def __init__(self, path="./"):
        self._proj = Project(path)

    def set_path(self, path="./"):
        """Set current project path(default './')."""
        self._proj = Project(path)
        return self

    def add_env(self, name: str, template: str):
        """Add an environment to the project.

        :param name: Name of the env.
        :param template: Template of the env.
        Using `list_env_templates` to see all
        available env templates.
        """
        self._proj.add_env(name, template)

    def list_env_templates(self):
        """List all available env templates."""
        all_temps = '\n'.join(list_env_templates())
        logger.info("Available env templates: \n"+all_temps)

    def create_project(self, path: str):
        """Create a project to specific path."""
        proj = Project(path)
        proj.create()
        self._proj = proj


class CLI():
    def __init__(self):
        # command groups
        self.project = ProjectManager()


if __name__ == "__main__":
    import fire
    fire.Fire(CLI)
