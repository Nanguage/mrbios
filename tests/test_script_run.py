import shutil
import os
from pathlib import Path

from mrbios.cli import CLI, EnvBuild
from mrbios.core.env_build import CondaEnvBuild



def setup_project(cli: "CLI", test_proj_path: str):
    project = cli.project
    project.create(test_proj_path)
    project._proj.add_task("TestTask", "Test")
    return project


def build_envs(cli):
    env_build = cli.env
    env_build.build_all()
    return env_build


def clear_stuff(env_build: EnvBuild, test_out, test_proj_path):
    os.remove(test_out)
    env_build.clear_all()
    shutil.rmtree(test_proj_path)


def test_py_script_run(cli: "CLI", test_proj_path: str):
    project = setup_project(cli, test_proj_path)
    # py-env and py-script
    project._proj.add_env("py-env", "py-env")
    project._proj.add_script("TestTask", "TestScript-py", "py-script", "Test")
    env_build = build_envs(cli)
    # Run py-script
    script_run = cli.script
    test_out = Path("./test_hello.txt")
    script_run.run(
        "TestTask/TestScript-py",
        name="world", times=10, out=test_out,
    )
    assert test_out.exists()
    clear_stuff(env_build, test_out, test_proj_path)


def test_R_script_run(cli: "CLI", test_proj_path: str):
    project = setup_project(cli, test_proj_path)
    # R-env and R-script
    project._proj.add_env("R-env", "r-env")

    # simplify the env build config
    env_build = CondaEnvBuild.from_config_file(
        f"{test_proj_path}/Environments/R-env/build.yaml")
    env_build.config["conda"]["deps"] = ["r-base==4.1.2"]
    env_build.config["R"] = {
        "cran": {
            "mirror": "https://mirrors.tuna.tsinghua.edu.cn/CRAN/",
            "deps": ["optparse"],
        }
    }
    env_build.write_to_config_file(
        f"{test_proj_path}/Environments/R-env/build.yaml")
    project._proj.add_script("TestTask", "TestScript-R", "r-script", "Test")

    env_build = build_envs(cli)
    # Run R-script
    script_run = cli.script
    test_out = Path("./test_hello.txt")
    script_run.run(
        "TestTask/TestScript-R",
        name="world", times=10, out=test_out,
    )
    assert test_out.exists()
    clear_stuff(env_build, test_out, test_proj_path)
