import abc

class Reader(abc.ABC):
    """
    Абстрактный класс для чтения файлов
    """
    @abc.abstractmethod
    def read_file(self, filepath : str) -> str:
        """
        Прочитать файл в строку
        Args:
            filepath(str) : путь к файлу
        """
        pass
    
    @abc.abstractmethod
    def read_dir(self, dir : str) -> list[str]:
        """
        Прочитать все файлы из директории в список строк
        Args:
            dir(str) : путь к директории
        """
        pass
    
    def pretify(self, text : str) -> str:
        """
        Удалить из строки служебные пробелы и прочую мерзость
        Args:
            text(str) : обрабатываемая строка
        """
        text = text.replace('\xa0', ' ')
        text = text.replace('*', '')
        return text
        