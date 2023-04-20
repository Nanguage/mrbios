import shutil

from mrbios.core.platform import Platform
from mrbios.cli import ProjectManager


TEST_PROJ = "./TestProj4"


def setup_project():
    project = ProjectManager()
    project.create(TEST_PROJ)
    project._proj.add_task("TestTask", "Test")
    project._proj.add_env("py-env", "py-env")
    project._proj.add_script("TestTask", "TestScript-py", "py-script", "Test")
    return project


def clear_stuff():
    shutil.rmtree(TEST_PROJ)


def test_platform():
    setup_project()
    platform = Platform(TEST_PROJ)
    assert len(platform.app.task_table.table) == 1
    clear_stuff()
