import sys
import pytest
from mrbios.cli import CLI


def pytest_sessionstart(session):
    sys.path.insert(0, "./")


@pytest.fixture
def test_proj_path() -> str:
    return "./TestProj"


@pytest.fixture
def cli(test_proj_path) -> "CLI":
    _cli = CLI()
    _cli.set_current_project(test_proj_path)
    return _cli
