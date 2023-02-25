import shutil
import io

import pytest

from mrbios.cli import ProjectManager


TEST_PROJ = "./TestProj"


def test_create():
    pr = ProjectManager()
    pr.create(TEST_PROJ)
    assert pr._proj.name == TEST_PROJ.removeprefix("./")
    assert pr._proj.path.exists()
    assert pr._proj.sub_paths.env.exists()
    assert pr._proj.sub_paths.format.exists()
    assert pr._proj.sub_paths.pipe.exists()
    assert pr._proj.sub_paths.task.exists()
    assert (pr._proj.path / "README.md").exists()
    shutil.rmtree(TEST_PROJ)


def test_list_env_templates():
    pr = ProjectManager()
    pr.set_path(TEST_PROJ)
    pr.list_env_templates()


def test_add_env(monkeypatch):
    pr = ProjectManager()
    pr.create(TEST_PROJ)
    with pytest.raises(IOError):
        pr.add_env("test_py", "not_exist")

    monkeypatch.setattr('sys.stdin', io.StringIO('py-env'))
    pr.add_env("test_py")
    pr.add_env("test_py", "py-env")  # aleardy exist
    envs = pr._proj.get_envs()
    assert len(envs) == 1
    env_path = pr._proj.sub_paths.env / "test_py"
    assert env_path.exists()
    assert (env_path / "build.yaml").exists()
    pr.list_envs()
    monkeypatch.setattr('sys.stdin', io.StringIO('y'))
    pr.remove_env("test_py")
    envs = pr._proj.get_envs()
    assert len(envs) == 0
    with pytest.raises(IOError):
        monkeypatch.setattr('sys.stdin', io.StringIO('y'))
        pr.remove_env("not_exist")
    shutil.rmtree(TEST_PROJ)


def test_add_file_type(monkeypatch):
    pr = ProjectManager()
    pr.create(TEST_PROJ)
    monkeypatch.setattr('sys.stdin', io.StringIO('The expression matrix.'))
    pr.add_file_type("ExpMat")
    assert len(pr._proj.get_file_types()) == 1
    pr.add_file_type("ExpMat", "The expression matrix.")
    ft_path = pr._proj.sub_paths.format / "ExpMat"
    assert ft_path.exists()
    assert (ft_path / "README.md").exists()
    pr.list_file_types()
    monkeypatch.setattr('sys.stdin', io.StringIO('y'))
    pr.remove_file_type("ExpMat")
    assert len(pr._proj.get_file_types()) == 0
    with pytest.raises(IOError):
        monkeypatch.setattr('sys.stdin', io.StringIO('y'))
        pr.remove_file_type("not_exist")
    shutil.rmtree(TEST_PROJ)
