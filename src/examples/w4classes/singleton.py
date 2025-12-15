import inspect
import os
from pathlib import Path
from typing_extensions import Self


class Config:
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        current_dir = Path(
            os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        )

        self._root_dir = current_dir.parent.parent
        # self.param1: str | int | None = None

    @property
    def root_dir(self) -> Path:
        return self._root_dir




# -------------
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyClass(metaclass=Singleton):
    pass


if __name__ == "__main__":

    cfg1 = Config()
    print(cfg1.root_dir)
    # Плохой пример, только для проверки
    cfg1.param1 = 1
    print(cfg1.param1)

    cfg2 = Config()
    print(cfg2.param1)