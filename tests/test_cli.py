from pathlib import Path
import shutil

from mrbios.cli import CLI
from mrbios.utils.user_setting import DEFAULT_SETTING_PATH, UserSetting
from mrbios.core.project import path_is_project



def test_cli(cli: "CLI", test_proj_path: str):
    assert DEFAULT_SETTING_PATH.exists()
    cli.project.create(test_proj_path)
    assert path_is_project(Path(test_proj_path))
    assert not path_is_project(Path.cwd())
    proj_path = Path(test_proj_path).absolute()
    assert cli._user_setting.attrs["project_path"] == str(proj_path)
    shutil.rmtree(proj_path)


def test_usersetting():
    test_path = Path("./for_test/test.json")
    user_setting = UserSetting(test_path)
    assert str(user_setting.path) == str(test_path)
    assert user_setting.path.exists()
    shutil.rmtree(test_path.parent)
