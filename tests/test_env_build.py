import shutil
import io
from subprocess import CalledProcessError

import pytest

from mrbios.cli import EnvBuild, ProjectManager
from mrbios.utils.misc import command_exist


TEST_PROJ = "./TestProj2"


def test_command_exist():
    assert command_exist("conda")
    assert command_exist("not_exist_command")


def test_build_env(monkeypatch):
    project = ProjectManager()
    project.create(TEST_PROJ)
    env_build = EnvBuild(TEST_PROJ)
    env_build.build()
    env_build._proj.add_env("test1", "py-env")
    env_build._proj.add_env("test2", "py-env")
    monkeypatch.setattr(
        "sys.stdin", io.StringIO("test1"))
    env_build.build()
    assert env_build._proj.get_envs()['test1'].is_built
    monkeypatch.setattr(
        "sys.stdin", io.StringIO("test1\ny"))
    env_build.delete()
    assert not env_build._proj.get_envs()['test1'].is_built
    env_build.build_all()
    assert env_build._proj.get_envs()['test1'].is_built
    assert env_build._proj.get_envs()['test2'].is_built
    env_build.run("test1", "pip", "install", "h5py")
    with pytest.raises(CalledProcessError):
        env_build.run("test1", "not_exist_command")
    env_build.clear_all()
    assert not env_build._proj.get_envs()['test1'].is_built
    assert not env_build._proj.get_envs()['test2'].is_built
    env_build.run("test1", "pip", "install", "h5py")
    env_build.list()
    shutil.rmtree(TEST_PROJ)
