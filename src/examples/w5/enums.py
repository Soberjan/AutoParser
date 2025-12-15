from abc import ABC, abstractmethod
from enum import Enum
import os
from typing import Any


class FileTypes(Enum):
    UNKNOWN = "UNK"
    PDF = ".pdf"
    DOCX = ".docx"

    @classmethod
    def _missing_(cls, value: object) -> Any:
        return cls.UNKNOWN


def print_ext(ext: FileTypes):
    if ext == FileTypes.PDF:
        print(f"{ext} is pdf")
    elif ext == FileTypes.DOCX:
        print(f"{ext} is docx")
    else:
        print(f"{ext} not supported")


extensions = [".pdf", ".docx", ".rtf"]
for e in extensions:
    print_ext(FileTypes(e.lower()))


# ------------------------
class Reader(ABC):
    @abstractmethod
    def read(self, file_name) -> str: ...


class PDFReader(Reader):
    def read(self, file_name):
        return f"text from {file_name} - pdf"


class DOCXReader(Reader):
    def read(self, file_name):
        return f"text from {file_name} - docx"


READERS = {
    FileTypes.PDF: PDFReader,
    FileTypes.DOCX: DOCXReader,
}


def read_file(file_name):
    _, ext = os.path.splitext(file_name)
    file_type = FileTypes(ext)

    if file_type != FileTypes.UNKNOWN:
        reader = READERS[file_type]()
        return reader.read(file_name)


print(read_file("a.doc"))
