import os

# from telethon import TelegramClient
from telethon.sync import TelegramClient

from utils.logger import logger
from config import Config
from fetcher.fetcher import Fetcher

class TelegramFetcher(Fetcher):
    """
    Класс для скачивания резюме из чата в телеграме
    """
    def __init__(self, dialogue_id : str = Config.tg_dialogue_id, download_path : str = Config.download_folder):
        self.dialogue_id = dialogue_id
        self.download_path = download_path

    def connect(self, api_id : str = Config.tg_api_id, api_hash : str = Config.tg_api_hash):
        """
        Метод для подключения к телеге
    
        Args:
            api_id(str) : айди апи телеграма
            api_id(str) : хэш апи телеграма
        """
        self.api_id = api_id
        self.api_hash = api_hash
        
        logger.info('Подключение к клиенту телеграма')
        self.client = TelegramClient('parser_session', self.api_id, self.api_hash)
        self.client.start()
        
    def disconnect(self):
        """
        Метод для отключения от телеги
        """
        self.client.disconnect()
    
    def download_files(self, new : bool = False):
        """
        Метод для скачивания резюме
        
        Args:
            new(bool) : если true, скачиваем только новые файлы, иначе - все
        """
        entity = self.client.get_entity(self.dialogue_id)
        dialog = self.client.get_dialogs(limit=None)
        dialog = next(d for d in dialog if d.id == entity.id)

        last_read_id = dialog.dialog.read_inbox_max_id if new else 0
        logger.info(last_read_id)
        
        for message in self.client.iter_messages(entity, min_id=last_read_id):
            if message.document:
                filename = message.document.attributes[0].file_name
                __, ext = os.path.split(filename)
                
                if ext == '.pdf' or ext == '.docx':
                    path = message.download_media(os.path.join(self.download_path, filename))
                    logger.info(f'Файл {filename} скачан в {path}')
            
            self.client.mark_read(entity, message.id)

if __name__ == '__main__': # pragma : no cover
    Config.init()
    telegram_fetcher = TelegramFetcher()
    telegram_fetcher.connect()
    telegram_fetcher.disconnect()
    telegram_fetcher.download_files()
    logger.info('nigger')