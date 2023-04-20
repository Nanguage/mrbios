import shutil
import io
from subprocess import CalledProcessError

import pytest

from mrbios.cli import CLI
from mrbios.utils.misc import command_exist
from mrbios.core.env_build import RConfig


def test_command_exist():
    assert command_exist("conda")
    assert not command_exist("not_exist_command")


def test_build_env(monkeypatch, test_proj_path, cli: "CLI"):
    project = cli.project
    project.create(test_proj_path)
    env_build = cli.env
    env_build.build()
    env_build._proj.add_env("test1", "py-env")
    env_build._proj.add_env("test2", "py-env")
    monkeypatch.setattr(
        "sys.stdin", io.StringIO("test1"))
    env_build.build()
    env_test1 = env_build._proj.get_envs()['test1']
    assert env_test1.build_name == (
        test_proj_path.removeprefix("./") + "-test1")
    assert env_test1.is_built
    print(repr(env_test1))
    monkeypatch.setattr(
        "sys.stdin", io.StringIO("test1\ny"))
    env_build.delete()
    assert not env_build._proj.get_envs()['test1'].is_built
    env_build.build_all()
    assert env_build._proj.get_envs()['test1'].is_built
    assert env_build._proj.get_envs()['test2'].is_built
    env_build.run("pip install h5py", "test1")
    with pytest.raises(CalledProcessError):
        env_build.run("not_exist_command", "test1")
    monkeypatch.setattr(
        "sys.stdin", io.StringIO("test1"))
    env_build.rebuild()
    env_build.rebuild_all()
    env_build.clear_all()
    env_test1 = env_build._proj.get_envs()['test1']
    assert not env_test1.is_built
    assert not env_build._proj.get_envs()['test2'].is_built
    print(repr(env_test1))
    env_build.run("pip install h5py", "test1")
    env_build.list()
    shutil.rmtree(test_proj_path)


def test_build_R_env(monkeypatch, cli: "CLI", test_proj_path):
    project = cli.project
    project.create(test_proj_path)
    env_build = cli.env
    env_build._proj.add_env("test3", "r-env")
    monkeypatch.setattr(
        "sys.stdin", io.StringIO("test3"))
    env_build.build()
    assert env_build._proj.get_envs()['test3'].is_built
    env_build.run("Rscript -e library(devtools)", "test3")
    env_build.run("Rscript -e library(BiocManager)", "test3")
    env_build.run("Rscript -e library(GenomicRanges)", "test3")
    monkeypatch.setattr("sys.stdin", io.StringIO("y"))
    env_build.delete("test3")
    shutil.rmtree(test_proj_path)


def test_RConfig():
    conf = RConfig({
        "cran": {
            "deps": ["devtools", "BiocManager"],
        },
        "bioconductor": {
            "deps": ["GenomicRanges", "DESeq2"],
        },
        "github": {
            "deps": ["hadley/devtools", "hadley/httr"]
        }
    })
    conf.get_cran_command()
    conf.get_bioconductor_command()
    conf.get_devtools_command()


def test_update_env(test_proj_path: str):
    cli = CLI()
    project = cli.project
    project.create(test_proj_path)
    project.add_env("test1", "py-env")
    project.add_env("test2", "py-env")
    env_build = cli.env
    env_build.build_all()
    test1_env = project._proj.get_envs()['test1']
    test1_config = test1_env.build_config
    test1_config.config['pip']['deps'] = ['h5py']
    test1_config.write_to_config_file(
        f"{test1_env.path}/build.yaml"
    )
    env_build.update_all()
    env_build.run("python -c 'import h5py'", "test1")
    env_build.update("test2")
    env_build.clear_all()
    shutil.rmtree(test_proj_path)
