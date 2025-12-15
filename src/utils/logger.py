import os
import sys

import loguru
from loguru import logger
from config import Config

def configure_logger(log_path : str = None, log_level: str = None, log_format: str = None) -> None:
    """Создаем логер который выводит данные в файл и в консоль

    Args:
        log_path (_type_): Путь для файла с логами
        log_level (str): Уровень логгирования
        log_format (str): Формат логов
    """

    level = log_level if log_level else Config.log_level
    format = log_format if log_format else Config.log_format

    loguru.logger.remove()
    loguru.logger.add(sys.stdout, level=level, format=format)
    
    file = log_path if log_path else Config.log_file
    
    if file:
        loguru.logger.add(file, level=level, format=format)
