import os

from pypdf import PdfReader

from reader.abc_reader import Reader

class ReaderPDF(Reader):
    """
    Класс для чтения pdf файлов
    """
    def read_file(self, filepath : str) -> str:
        """
        Прочитать файл в строку
        Args:
            filepath(str) : путь к файлу
        """
        reader = PdfReader(filepath)
        full_text = '\n'.join(page.extract_text() for page in reader.pages)
        full_text = self.pretify(full_text)
        return full_text
    
    def read_dir(self, dir : str) -> list[str]:
        """
        Прочитать все файлы из директории в список строк
        Args:
            dir(str) : путь к директории
        """
        read_files = []
        for file in os.listdir(dir):
            filename, file_extension = os.path.splitext(file)
            if file_extension == '.pdf':
                read_files.append(self.read_file(os.path.join(dir, file)))
        return read_files