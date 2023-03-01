import shutil
import io

from mrbios.cli import EnvBuild, ProjectManager


TEST_PROJ = "./TestProj2"


def test_build_env(monkeypatch):
    project = ProjectManager()
    project.create(TEST_PROJ)
    env_build = EnvBuild(TEST_PROJ)
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
    env_build.clear_all()
    assert not env_build._proj.get_envs()['test1'].is_built
    assert not env_build._proj.get_envs()['test2'].is_built
    shutil.rmtree(TEST_PROJ)
