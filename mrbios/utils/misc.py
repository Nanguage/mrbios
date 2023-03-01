import shutil


def command_exist(command: str) -> bool:
    if shutil.which(command) is None:
        return False
    else:
        return True
