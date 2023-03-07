from pathlib import Path
import shutil

from mrbios.cli import CLI
from mrbios.utils.user_setting import DEFAULT_SETTING_PATH, UserSetting
from mrbios.core.project import path_is_project


TEST_PROJ = "./TestProj3"


def test_cli():
    cli = CLI()
    assert DEFAULT_SETTING_PATH.exists()
    cli.project.create(TEST_PROJ)
    assert path_is_project(Path(TEST_PROJ))
    assert not path_is_project(Path.cwd())
    proj_path = Path(TEST_PROJ).absolute()
    assert cli._user_setting.attrs["project_path"] == str(proj_path)
    shutil.rmtree(proj_path)


def test_usersetting():
    test_path = Path("./for_test/test.json")
    user_setting = UserSetting(test_path)
    assert str(user_setting.path) == str(test_path)
    assert user_setting.path.exists()
    shutil.rmtree(test_path.parent)
