import shutil

from mrbios.core.platform import Platform
from mrbios.cli import CLI


def setup_project(cli: "CLI", test_proj_path: str):
    project = cli.project
    project.create(test_proj_path)
    project._proj.add_task("TestTask", "Test")
    project._proj.add_env("py-env", "py-env")
    project._proj.add_script("TestTask", "TestScript-py", "py-script", "Test")
    return project


def clear_stuff(test_proj_path: str):
    shutil.rmtree(test_proj_path)


def test_platform(test_proj_path):
    setup_project()
    platform = Platform(test_proj_path)
    assert len(platform.app.task_table.table) == 1
    clear_stuff()
