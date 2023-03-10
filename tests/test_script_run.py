import shutil
import os

from mrbios.cli import ScriptRun, ProjectManager, EnvBuild


TEST_PROJ = "./TestProj3"


def test_script_run():
    project = ProjectManager()
    project.create(TEST_PROJ)
    project._proj.add_env("py-env", "py-env")
    project._proj.add_task("TestTask", "Test")
    project._proj.add_script("TestTask", "TestScript", "py-script", "Test")
    env_build = EnvBuild()
    env_build.build_all()
    script_run = ScriptRun()
    test_out = "./test_hello.txt"
    script_run.run(
        "TestTask/TestScript",
        name="world", times=10, out=test_out,
    )
    os.remove(test_out)
    env_build.clear_all()
    shutil.rmtree(TEST_PROJ)
