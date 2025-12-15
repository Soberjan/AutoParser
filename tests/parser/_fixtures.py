import pytest

from src.parser.parser import Parser


@pytest.fixture
def new_doc_parser() -> Parser:
    """Новая модель для тестов.
    Всегда новая для корректности тестов.
    Если нужно переиспользовать модель, то используем @pytest.fixture(scope="session")


    Returns:
        Model: Готовая модель для тестов.
    """
    return Parser()
