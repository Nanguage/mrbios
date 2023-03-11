import shutil
import os
from pathlib import Path

from mrbios.cli import ScriptRun, ProjectManager, EnvBuild
from mrbios.core.env_build import CondaEnvBuild


TEST_PROJ = "./TestProj3"


def setup_project():
    project = ProjectManager()
    project.create(TEST_PROJ)
    project._proj.add_task("TestTask", "Test")
    return project


def build_envs():
    env_build = EnvBuild()
    env_build.build_all()
    return env_build


def clear_stuff(env_build: EnvBuild, test_out):
    os.remove(test_out)
    env_build.clear_all()
    shutil.rmtree(TEST_PROJ)


def test_py_script_run():
    project = setup_project()
    # py-env and py-script
    project._proj.add_env("py-env", "py-env")
    project._proj.add_script("TestTask", "TestScript-py", "py-script", "Test")
    env_build = build_envs()
    # Run py-script
    script_run = ScriptRun()
    test_out = Path("./test_hello.txt")
    script_run.run(
        "TestTask/TestScript-py",
        name="world", times=10, out=test_out,
    )
    assert test_out.exists()
    clear_stuff(env_build, test_out)


def test_R_script_run():
    project = setup_project()
    # R-env and R-script
    project._proj.add_env("R-env", "r-env")

    # simplify the env build config
    env_build = CondaEnvBuild.from_config_file(
        f"{TEST_PROJ}/Environments/R-env/build.yaml")
    env_build.config["conda"]["deps"] = ["r-base==4.1.2"]
    env_build.config["R"] = {
        "cran": {
            "mirror": "https://mirrors.tuna.tsinghua.edu.cn/CRAN/",
            "deps": ["optparse"],
        }
    }
    env_build.write_to_config_file(
        f"{TEST_PROJ}/Environments/R-env/build.yaml")
    project._proj.add_script("TestTask", "TestScript-R", "r-script", "Test")

    env_build = build_envs()
    # Run R-script
    script_run = ScriptRun()
    test_out = Path("./test_hello.txt")
    script_run.run(
        "TestTask/TestScript-R",
        name="world", times=10, out=test_out,
    )
    assert test_out.exists()
    clear_stuff(env_build, test_out)
