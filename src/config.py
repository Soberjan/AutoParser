import os
import json

class Config:
    """
    Класс для хранения настроек приложения
    """
    log_level = None
    log_format = None
    log_file = None
    
    parser_output_path = None
    parser_input_path = None
    
    download_folder = None
    imap_email = None
    imap_password = None
    imap_server = None
    imap_folder = None
    
    tg_api_id = None
    tg_api_hash = None
    tg_dialogue_id = None
    
    timestamp_dict = None
    
    db_host = None
    db_name = None
    db_user = None
    db_password = None
    
    @classmethod
    def init(cls, log_level : str = None, log_format : str = None, 
                 log_file : str = None, parser_output_path : str = None,
                 parser_input_path : str = None,
                 download_folder : str = None, imap_email : str = None,
                 imap_password : str = None, imap_server : str = None,
                 imap_folder : str = None,
                 tg_api_id : str = None, tg_api_hash : str = None,
                 tg_dialogue_id : str = None, psql_password : str = None,
                 db_host : str = None, db_name : str = None, db_user : str = None,
                 db_password : str = None):
        """
        Функция для инициализации конфига
        Args:
            str(log_level) : Уровень логирования
            str(log_format) : Формат логирования
            str(log_file) : Путь, по которому сохраняем логи
            str(parser_output_path) : Папка, куда парсер сохраняет обработанные файлы
            str(parser_input_path) : Папка, откуда парсер берет файлы
            str(download_folder) : Папка, в которую сохраняем скачанные файлы
            str(imap_email) : Почта, с которой будут браться данные
            str(imap_password) : Пароль для аймап приложнения
            str(imap_server) : Аймап сервер
            str(imap_folder) : Фолдер аймап, с которым работает
            str(tg_api_id) : Айди тг приложения
            str(tg_api_hash) : Хэш тг приложения
            str(tg_dialogue_id) : Айди диалога в тг, с которого скачиваем файлы
            str(db_host) : хост датабазы
            str(db_name) : имя датабазы
            str(db_user) : юзер датабазы
            str(db_password) : пароль датабазы
        """
        
        # Сделать этот кусок через цикл!        
        cls.log_level = log_level if log_level else os.environ.get('LOG_LEVEL')
        cls.log_format = log_format if log_format else os.environ.get('LOG_FORMAT')
        cls.log_file = log_file if log_file else os.environ.get('LOG_FILE')
        
        cls.parser_output_path = parser_output_path if parser_output_path else os.environ.get('PARSER_OUTPUT_DIR')
        cls.parser_input_path = parser_input_path if parser_input_path else os.environ.get('PARSER_INPUT_DIR')
        
        cls.download_folder = download_folder if download_folder else os.environ.get('DOWNLOAD_FOLDER')
        cls.imap_email = imap_email if imap_email else os.environ.get('IMAP_EMAIL')
        cls.imap_password = imap_password if imap_password else os.environ.get('IMAP_PASSWORD')
        cls.imap_server = imap_server if imap_server else os.environ.get('IMAP_SERVER')
        cls.imap_folder = imap_folder if imap_folder else os.environ.get('IMAP_FOLDER')
        
        cls.tg_api_id = tg_api_id if tg_api_id else os.environ.get('TG_API_ID')
        cls.tg_api_hash = tg_api_hash if tg_api_hash else os.environ.get('TG_API_HASH')
        cls.tg_dialogue_id = tg_dialogue_id if tg_dialogue_id else os.environ.get('TG_DIALOGUE_ID')
        
        cls.db_host = db_host if db_host else os.environ.get('DB_HOST')
        cls.db_name = db_name if db_name else os.environ.get('DB_NAME')
        cls.db_user = db_user if db_user else os.environ.get('DB_USER')
        cls.db_password = db_password if db_password else os.environ.get('DB_PASSWORD')