import pytest
from pydantic import ValidationError
from examples.w3testing.module2.unit import Unit

from helpers import BasicTestCase, case_names, change_data, create_object
from tests.examples.w3testing.module2.test_material import valid_material
from tests.examples.w3testing.module2.test_unit_type import valid_unit_type


valid_unit = {"name": "u1", "content": [valid_material], "type_": valid_unit_type}

valid_unit_empty_content = change_data(
    valid_unit,
    content=[],
)

bad_unit_wo_content = change_data(
    valid_unit,
    content=None,
)

cases = [
    BasicTestCase(valid_unit, None, None, "valid"),
    BasicTestCase(valid_unit_empty_content, None, None, "empty_content"),
    BasicTestCase(bad_unit_wo_content, None, ValidationError, "wo_content"),
]


@pytest.mark.parametrize("tc", cases, ids=case_names(cases))
def test_material(tc: BasicTestCase):
    create_object(tc, Unit)
