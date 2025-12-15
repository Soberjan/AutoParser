import pytest

from examples.w3testing.module1.model import Model


@pytest.fixture
def new_model() -> Model:
    """Новая модель для тестов.
    Всегда новая для корректности тестов.
    Если нужно переиспользовать модель, то используем @pytest.fixture(scope="session")


    Returns:
        Model: Готовая модель для тестов.
    """
    return Model(0)
