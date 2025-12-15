from typing import Any, ContextManager, NamedTuple
from contextlib import nullcontext as does_not_raise

import pytest

from examples.w3testing.module1.model import Model
from examples.w3testing.module1.errors import MethodError
from tests.examples.w3testing.module1.new_model import new_model
from helpers import case_names

# один тест на каждую функцию, меняются только параметры
# параметры именованы и их можно вынести в отдельный файл


TestCaseB = NamedTuple(
    "TestCaseB",
    [("value", Any), ("result_set", bool), ("result_b", Any), ("name", str)],
)
cases_b = [
    TestCaseB(value=1, result_set=True, result_b=1, name="valid"),
    TestCaseB(value="2", result_set=False, result_b=None, name="false_wo_b"),
]

TestCaseCalculate = NamedTuple(
    "TestCaseCalculate",
    [
        ("value_b", Any),
        ("value_method", str),
        ("result", Any),
        ("expectation", ContextManager),
        ("name", str),
    ],
)
cases_calculate = [
    TestCaseCalculate(
        value_b=1,
        value_method="m1",
        result=2,
        expectation=does_not_raise(),
        name="valid_m1",
    ),
    TestCaseCalculate(
        value_b=1,
        value_method="m2",
        result="-1",
        expectation=does_not_raise(),
        name="valid_m2",
    ),
    TestCaseCalculate(
        value_b=None,
        value_method="m1",
        result="-1",
        expectation=pytest.raises(ValueError),
        name="fail_wo_b",
    ),
    TestCaseCalculate(
        value_b=1,
        value_method="unk_m",
        result="-1",
        expectation=pytest.raises(MethodError),
        name="unknown_method",
    ),
]


# Параметры в декораторе
@pytest.mark.parametrize("case", cases_b, ids=case_names(cases_b))
def test_set_b(new_model: Model, case: TestCaseB):
    assert new_model.set_b(case.value) == case.result_set
    assert new_model._b == case.result_b


@pytest.mark.parametrize("case", cases_calculate, ids=case_names(cases_calculate))
def test_calculate(
    new_model: Model,
    case: TestCaseCalculate,
):
    with case.expectation:
        new_model.set_b(case.value_b)
        assert new_model.calculate(case.value_method) == case.result
