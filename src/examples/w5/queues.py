import queue
import random
import threading
from time import sleep
# from utils.logger import configure_logger, logger


# logger = create_logger(level="DEBUG")
# configure_logger()
q = queue.Queue()


def parser(name, work_time):
    print(f"Работаем с {name} длительностью {work_time}")
    sleep(work_time)
    print(f"Закончился {name}")


def worker():
    while True:
        item = q.get()
        func = item[0]
        args = item[1:]
        func(*args)
        q.task_done()


def run():
    threading.Thread(target=worker, daemon=True).start()

    for i in range(15):
        print(f"Добавляем {i}")
        q.put([parser, i, random.randint(0, 2)])
        sleep(1)

    q.join()
    print("DONE...")


if __name__ == "__main__":
    run()

# Варианты параллельного выполнения
# 1. threading
# 2. multiprocessing
# 3. asyncio

# TODO: Планы
# # REST API - fastapi - sync - SQL
# # REST API - DRF - sync  ORM
# endpoints: get_cv_from_file/ -> BD
#         get_cv_list/ -> [id1, id2...]
#         get_cv/{id} -> {"name":"ssssss", ....}

# front -> endpoints
