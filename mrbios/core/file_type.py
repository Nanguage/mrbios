import typing as T

from .dir_obj import DirObj
if T.TYPE_CHECKING:
    from .file_format import FileFormat


class FileType(DirObj):
    @property
    def file_formats(self) -> list["FileFormat"]:
        from .file_format import FileFormat
        formats = []
        for p in self.path.iterdir():
            if not p.is_dir():
                continue
            ff = FileFormat(p.name, self.path)
            formats.append(ff)
        return formats
