import abc

class Fetcher(abc.ABC):    
    """
    Абстрактный класс для загрузки файлов из разных источников
    """
    @abc.abstractmethod    
    def download_files(self, new : bool = False, download_folder : str = None):
        """
        Скачиваем файлы в download folder

        Args:
            new(bool) : скачиваем только новые файлы или все файлы
            download_folder(str) : путь к папке куда скачиваем файлы
        """
        pass

    @abc.abstractmethod    
    def connect(self):
        """
        Метод для установления соединения с источником
        """
        pass
    