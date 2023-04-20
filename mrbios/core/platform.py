import typing as T
from pathlib import Path
from executor.http.server import create_app, ServerSetting, run_app
from executor.engine.launcher import AsyncLauncher
from .project import Project


class Platform():
    def __init__(
            self, proj_path: str | Path,
            server_settings: T.Optional[dict] = None,):
        self.project = Project(proj_path)
        server_settings = server_settings or {}
        self.server_settings = ServerSetting(**server_settings)
        self.app = self.get_executor_app()

    def get_executor_app(self):
        app = create_app(self.server_settings)
        for task in self.project.get_tasks().values():
            for script in task.scripts:
                script_runner = script.runner
                launcher = AsyncLauncher(
                    script_runner.get_run_func(),
                    job_type='process',
                    name=script.name,
                    tags=[task.name]
                )
                app.task_table.register(launcher)
        return app

    def run_server(
            self, host="127.0.0.1", port=5000, **kwargs):  # pragma: no cover
        run_app(self.app, host=host, port=port, **kwargs)
