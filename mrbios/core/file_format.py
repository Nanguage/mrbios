from .dir_obj import DirObj
from .file_type import FileType


class FileFormat(DirObj):
    def file_type(self) -> FileType:
        parent = self.path.parent
        return FileType(parent.name, parent)
