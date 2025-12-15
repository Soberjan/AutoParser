from typing import Tuple
import pytest

from examples.w3testing.module1.model import Model

# Пример как менять параметры в фикстурах


@pytest.fixture(scope="function")
def param_model(request: pytest.FixtureRequest) -> Tuple[Model, int]:
    """Новая модель для тестов с разными входными данными.

    Returns:
        Model: Готовая модель для тестов.
    """
    return Model(request.param), request.param


@pytest.mark.debug_only
@pytest.mark.parametrize("param_model", [0, 1], indirect=True)
def test_model_a(param_model: Tuple[Model, int]):
    assert param_model[0]._a == param_model[1]  # type: ignore
