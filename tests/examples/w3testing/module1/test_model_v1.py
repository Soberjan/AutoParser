import pytest
from examples.w3testing.module1.model import Model
from examples.w3testing.module1.errors import MethodError

# Всё в одном тесте, проверяет до первой ошибки


def test_model():
    m = Model(0)
    with pytest.raises(ValueError):
        m.calculate("m1")
    assert m.set_b(1)
    assert m.calculate("m1") == 2

    assert m.set_b("b2") == False  # type: ignore

    assert m.calculate("m2") == "-1"
    with pytest.raises(MethodError):
        m.calculate("unk_m")
