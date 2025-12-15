from enum import Enum
from typing import Any

from reader.docx_reader import ReaderDOCX
from reader.pdf_reader import ReaderPDF

class FileTypes(Enum): # pragma: no cover
    UNKNOWN = "UNK"
    PDF = ".pdf"
    DOCX = ".docx"

    @classmethod
    def _missing_(cls, value: object) -> Any:
        return cls.UNKNOWN

# pragma: no cover
READERS = {
    FileTypes.PDF: ReaderPDF(),
    FileTypes.DOCX: ReaderDOCX(),
}
