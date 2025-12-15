from time import sleep
from utils.logger import create_logger

from dotenv import load_dotenv


def main():
    logger = create_logger()
    while True:
        logger.info("Привет от Питона!")
        sleep(10)


if __name__ == "__main__":
    load_dotenv()
    main()
