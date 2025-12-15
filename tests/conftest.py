import pytest

import inspect
import os
import sys

from helpers import str_to_bool


current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))  # type: ignore
parent_dir = os.path.dirname(current_dir)  # type: ignore
sys.path.insert(0, parent_dir)  # type: ignore
sys.path.append("./src")

from src.config import Config

def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--debug_only",
        action="store_true",
        help="run the tests only in case of debug_only option enabled"
        "(marked with marker @pytest.mark.debug_only)",
    )


def pytest_runtest_setup(item: pytest.Item):
    # Запускать тесты в режиме локальной отладки
    run_debug = str_to_bool(os.environ.get("LOCAL_DEBUG", ""))
    if not run_debug and "debug_only" in item.keywords:
        pytest.skip(
            f"{item.name}. Запуск теста только в режиме локальной отладки.")


@pytest.fixture
def test_root_folder():
    """
    Абсолютный путь к корню тестов
    tests/conftest.py -> tests/
    """

    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def root_folder(test_root_folder: str) -> str:
    """Определение корня проекта.

    Returns:
        str: Абсолютный путь к корню проекта.
    """

    return os.path.dirname(test_root_folder)


@pytest.fixture
def writer():
    def w(message):
        w.written.append(message)

    w.written = []
    w.read = lambda: "".join(w.written)
    w.clear = lambda: w.written.clear()

    return w

@pytest.fixture
def config() -> Config:
    Config.init()
    return Config