import os

import imapclient
import pyzmail

from utils.decorators import timer
from utils.logger import logger
from config import Config
from fetcher.fetcher import Fetcher

class MailFetcher(Fetcher):
    """
    Класс для скачивания резюме с электронной почты
    """
    def __init__(self):
        self.connection = None
    
    def connect(self, email : str = Config.imap_email, password : str = Config.imap_password, imap_server : str = Config.imap_server):
        """
        Метод для установления соединения с источником
        
        email(str) : почта к которой подключаемся
        password(str) : пароль для нашего ай мап приложения
        imap_server(str) : ай мап сервер, к которому подключаемся
        """
        
        logger.info('Connecting to mail')
        self.connection = imapclient.IMAPClient(imap_server)
        self.connection.login(email, password)
    
    @timer
    def download_files(self, new : bool = False, download_folder : str = None, imap_folder : str = Config.imap_folder):
        """
        Cкачиваем резюме из электронной почты и складываем в директорию, указанную в переменной окружения

        Args:
            new(bool) : если true, скачиваем только новые файлы, иначе - все
            download_folder(str) : папка в которую скачиваем файлы
            imap_folder(str) : папка в ай мапе, которую обрабатываем
        """
        
        # мб сделать через рейз экспешн и учесть случаи, когда соединение разорвалось
        if self.connection == None:
            logger.error("Соединение не установлено")
            return 
        
        self.connection.select_folder(imap_folder)

        # last_mail_id = MsgIdObserver.last_mail_id() if new else 0
        
        search_flag = 'UNSEEN' if new else 'ALL'
        
        uids = self.connection.search([search_flag])
        
        download_folder = download_folder if download_folder else Config.download_folder

        for uid in uids:
            raw_message = self.connection.fetch([uid], ['BODY[]'])[uid][b'BODY[]']
            message = pyzmail.PyzMessage.factory(raw_message)
            
            for part in message.mailparts:
                if part.filename:
                    __, ext = os.path.splitext(part.filename)
                    if ext == '.pdf' or ext == '.docx':
                        file_to_save = os.path.join(download_folder, part.filename)
                        
                        with open(file_to_save, 'wb') as f:
                            f.write(part.get_payload())
                            logger.info(f'Файл {part.filename} скачан в {download_folder}')
        
        if uids:
            self.connection.add_flags(uids, [b'\\SEEN'])
    
    def _mark_as_unread(self, imap_folder : str = Config.imap_folder):
        """
        Скрытый метод, помечает все сообщения в ай мап папке непрочитанными
    
        Args:
            imap_folder(str) : папка в ай мапе, которую обрабатываем
        """
        self.connection.select_folder(imap_folder)
        uids = self.connection.search(['ALL'])
        
        self.connection.remove_flags(uids, [b'\\SEEN'])
        logger.info('Marked all mail messages as unread')
        
        
# if __name__ == '__main__':  
#     Config.init()
#     mail_fetcher = MailFetcher()
#     mail_fetcher.connect(Config.imap_email, Config.imap_password, Config.imap_server)
#     # mail_fetcher._mark_as_unread()

#     # mail_fetcher.download_files(new=False, download_folder='tmp/')