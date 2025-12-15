import pytest
from pydantic import ValidationError
from examples.w3testing.module2.unit_type import UnitType

from tests.helpers import BasicTestCase, case_names, create_object


valid_unit_type = {"name": "n1", "velocity": 12.4}

cases = [
    BasicTestCase(valid_unit_type, None, None, "valid"),
]


@pytest.mark.parametrize("tc", cases, ids=case_names(cases))
def test_material(tc: BasicTestCase):
    create_object(tc, UnitType)
