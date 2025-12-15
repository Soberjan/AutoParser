import os
import argparse
import threading
import time

from dotenv import load_dotenv

from config import Config
load_dotenv()
Config.init()
from utils.logger import logger, configure_logger
from parser.parser import Parser
import config
from fetcher.mail_fetcher import MailFetcher
from fetcher.telegram_fetcher import TelegramFetcher
from database.database import Database

if __name__ == '__main__': # pragma: no cover
    # print(Config.db_host)
    logger.info(config.__name__ + config.__file__)

    configure_logger()

    parser = argparse.ArgumentParser(description="My CLI app")
    subparsers = parser.add_subparsers(dest='command')

    parser_dir = subparsers.add_parser('parse_dir', help='Parse all cvs from specified directory')
    parser_dir.add_argument('--dir', type=str, default='', help='Dir to parse from')

    parser_mail = subparsers.add_parser('parse_mail', help='Parse from email')
    parser_mail.add_argument('-n', action='store_true', help='Parse only new messages')

    parser_tg = subparsers.add_parser('parse_tg', help='Parse from telegram')
    parser_tg.add_argument('-n', action='store_true',help='Parse only new messages')

    parser_listener = subparsers.add_parser('listen', help='Listen to mail and tg')
    
    args = parser.parse_args()
    
    db = Database()
    db.connect()
    doc_parser = Parser(db)
    
    if args.command == 'parse_dir':
        cvs_path = os.path.join(os.path.curdir, args.dir)
        doc_parser.parse_dir(cvs_path)
    
    # Эхэх, нужно эти мерзости тоже в свои методы внести, отрефакторю
    if args.command == 'parse_mail':
        mail_fetcher = MailFetcher()
        mail_fetcher.connect(Config.imap_email, Config.imap_password, Config.imap_server)
        doc_parser.parse_fetcher(mail_fetcher, args.n)
        
    if args.command == 'parse_tg':
        telegram_fetcher = TelegramFetcher() 
        telegram_fetcher.connect(Config.tg_api_id, Config.tg_api_hash)
        doc_parser.parse_fetcher(telegram_fetcher, args.n)
    
    if args.command == 'listen':
        mail_fetcher = MailFetcher()
        mail_fetcher.connect(Config.imap_email, Config.imap_password, Config.imap_server)
        
        telegram_fetcher = TelegramFetcher()
        telegram_fetcher.connect(Config.tg_api_id, Config.tg_api_hash)

        mail_thread = threading.Thread(target=doc_parser.listen_fetcher, args=(mail_fetcher))
        telegram_thread = threading.Thread(target=doc_parser.listen_fetcher, args=(telegram_fetcher))

        mail_thread.start()
        telegram_thread.start()

        while True:
            logger.info("Прослушиваем каналы связи")
            time.sleep(10)