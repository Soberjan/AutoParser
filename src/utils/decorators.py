import time
from utils.logger import logger


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        logger.info(
            f'Время выполнения метода {func.__name__}: {end-start:.4f}')
        return res
    return wrapper
