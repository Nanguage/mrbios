import shutil
import datetime
from pathlib import Path


def command_exist(command: str) -> bool:
    """Check if a command exists."""
    if shutil.which(command) is None:
        return False
    else:
        return True


def file_has_changed_after(
        file_path: str | Path,
        time_point: datetime.datetime) -> bool:
    """Check if a file has changed after a given time point."""
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return file_path.stat().st_mtime > time_point.timestamp()
