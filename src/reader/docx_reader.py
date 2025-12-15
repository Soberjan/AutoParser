import os

from docx import Document

from reader.abc_reader import Reader

class ReaderDOCX(Reader):
    """
    Класс для чтения docx файлов
    """
    def read_file(self, filepath : str) -> str:
        """
        Прочитать файл в строку
        Args:
            filepath(str) : путь к файлу
        """
        doc = Document(filepath)
        full_text = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
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
            if file_extension == '.docx':
                content = self.read_file(os.path.join(dir, file))
                content = self.pretify(content)
                read_files.append(content)
        return read_files