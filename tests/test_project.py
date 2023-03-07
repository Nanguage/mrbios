import shutil
import io

import pytest

from mrbios.cli import ProjectManager


TEST_PROJ = "./TestProj"


def test_create():
    pr = ProjectManager()
    with pytest.raises(IOError):
        pr._proj.check_exist()
    pr.create(TEST_PROJ)
    assert 'mrbios-version' in pr._proj.meta_info
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
    pr.set_working(TEST_PROJ)
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
    desc = 'The expression matrix.'
    monkeypatch.setattr('sys.stdin', io.StringIO(desc))
    pr.add_file_type("ExpMat")
    file_types = pr._proj.get_file_types()
    ft = file_types['ExpMat']
    assert ft.meta_info_path.exists()
    assert ft.meta_info['description'] == desc
    assert len(file_types) == 1
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


def test_add_file_format(monkeypatch):
    pr = ProjectManager()
    pr.create(TEST_PROJ)
    pr.add_file_type("ExpMat", "The exp table.")
    monkeypatch.setattr(
        "sys.stdin", io.StringIO("ExpMat\nThe txt format mat."))
    pr.add_file_format("TxtMat")
    with pytest.raises(IOError):
        pr._proj.add_file_format("NotExist", "Txt", "")
    with pytest.raises(IOError):
        pr._proj.remove_file_format("NotExist", "Txt")
    with pytest.raises(IOError):
        pr._proj.get_file_formats("NotExist")
    ft = pr._proj.get_file_types()['ExpMat']
    assert len(ft.file_formats) == 1
    fm = ft.file_formats[0]
    assert fm.file_type.path == ft.path
    assert fm.path.exists()
    assert (fm.path / 'example_file.txt').exists()
    assert (fm.path / 'README.md').exists()
    pr.list_file_formats('All')
    pr.list_file_formats("ExpMat")
    with pytest.raises(IOError):
        pr.list_file_formats("NotExist")
    monkeypatch.setattr('sys.stdin', io.StringIO('y'))
    pr.remove_file_format("ExpMat", "TxtMat")
    assert len(ft.file_formats) == 0
    shutil.rmtree(TEST_PROJ)


def test_add_task(monkeypatch):
    pr = ProjectManager()
    pr.create(TEST_PROJ)
    monkeypatch.setattr(
        "sys.stdin", io.StringIO("Test"))
    pr.add_task("TestTask")
    tasks = pr._proj.get_tasks()
    assert len(tasks) == 1
    assert tasks['TestTask'].path.exists()
    assert (tasks['TestTask'].path / "README.md").exists()
    pr.list_tasks()
    monkeypatch.setattr(
        "sys.stdin", io.StringIO("y"))
    pr.remove_task("TestTask")
    assert len(pr._proj.get_tasks()) == 0
    shutil.rmtree(TEST_PROJ)


def test_add_script(monkeypatch):
    pr = ProjectManager()
    pr.create(TEST_PROJ)
    pr.add_task("TestTask", "Test")
    monkeypatch.setattr(
        "sys.stdin", io.StringIO("TestTask\npy-script\nTest"))
    pr.add_script("TestScript")
    with pytest.raises(IOError):
        pr.add_script("Test2", "TestTask", "NotExists", "Test")
    with pytest.raises(IOError):
        pr.add_script("Test2", "NotExists", "py-script", "Test")
    task = pr._proj.get_tasks()['TestTask']
    assert len(task.scripts) == 1
    script = task.scripts[0]
    assert script.task.path == task.path
    assert script.path.exists()
    assert (script.path / "interface.yaml").exists()
    assert (script.path / "README.md").exists()
    assert (script.path / "run.py").exists()
    pr.list_scripts("TestTask")
    with pytest.raises(IOError):
        pr.list_scripts("NotExist")
    pr.list_scripts("All")
    with pytest.raises(IOError):
        monkeypatch.setattr("sys.stdin", io.StringIO("y"))
        pr.remove_script("NotExist", "TestScript")
    monkeypatch.setattr("sys.stdin", io.StringIO("y"))
    pr.remove_script("TestTask", "TestScript")
    scripts = pr._proj.get_scripts("TestTask")
    assert len(scripts) == 0
    shutil.rmtree(TEST_PROJ)
