import pytest
from examples.w3testing.module1.model import Model
from examples.w3testing.module1.errors import MethodError
from examples.w3testing.module1.new_model import new_model

# Каждая проверка в отдельном тесте, можно получить сразу все ошибки


def test_set_b_ok(new_model: Model):
    assert new_model.set_b(1)

    # в каждом из тестов возможны и доп. проверки,
    # например что установились правильные значения и т.д.
    assert new_model._b == 1  # type: ignore


def test_set_b_false(new_model: Model):
    assert new_model.set_b("b2") == False  # type: ignore


def test_calculate_m1(new_model: Model):
    new_model.set_b(1)
    assert new_model.calculate("m1") == 2


def test_calculate_m2(new_model: Model):
    new_model.set_b(1)
    assert new_model.calculate("m2") == "-1"


def test_calculate_no_b(new_model: Model):
    with pytest.raises(ValueError):
        new_model.calculate("m1")


def test_calculate_bad_method(new_model: Model):
    assert new_model.set_b(1)
    with pytest.raises(MethodError):
        new_model.calculate("unk_m")
