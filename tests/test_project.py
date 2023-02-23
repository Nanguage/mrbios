import shutil

from mrbios.cli import ProjectManager


TEST_PROJ = "./TestProj"


def test_create():
    pr = ProjectManager()
    pr.create(TEST_PROJ)
    assert pr._proj.path.exists()
    assert pr._proj.sub_paths.env.exists()
    assert pr._proj.sub_paths.format.exists()
    assert pr._proj.sub_paths.pipe.exists()
    assert pr._proj.sub_paths.task.exists()
    assert (pr._proj.path / "README.md").exists()
    shutil.rmtree(TEST_PROJ)


def test_add_env():
    pr = ProjectManager()
    pr.create(TEST_PROJ)
    pr.add_env("test_py", "py-env")
    env_path = pr._proj.sub_paths.env / "test_py"
    assert env_path.exists()
    assert (env_path / "build.yaml").exists()
    shutil.rmtree(TEST_PROJ)
