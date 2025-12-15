from typing import Any, ContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from examples.w3testing.module1.model import Model
from examples.w3testing.module1.errors import MethodError
from examples.w3testing.module1.new_model import new_model


# один тест на каждую функцию, меняются только параметры
# Параметры в декораторе
@pytest.mark.parametrize(
    "value, result_set, result_b", ((1, True, 1), ("2", False, None))
)
def test_set_b(new_model: Model, value: Any, result_set: bool, result_b: int | None):
    assert new_model.set_b(value) == result_set
    assert new_model._b == result_b  # type: ignore


@pytest.mark.parametrize(
    "value_b, value_method, result, expectation",
    (
        (1, "m1", 2, does_not_raise()),
        (1, "m2", "-1", does_not_raise()),
        (None, "m1", "-1", pytest.raises(ValueError)),
        (1, "unk_m", "1", pytest.raises(MethodError)),
    ),
)
def test_calculate(
    new_model: Model,
    value_b: int,
    value_method: str,
    result: Any,
    expectation: ContextManager,
):
    with expectation:
        new_model.set_b(value_b)
        assert new_model.calculate(value_method) == result
