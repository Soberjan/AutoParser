import pytest
from pydantic import ValidationError
from examples.w3testing.module2.material import Material

from tests.helpers import BasicTestCase, case_names, change_data, create_object


valid_material = {"id": "s1", "density": 125, "mass": 50, "volume": 0.4}

bad_id_material = change_data(
    valid_material,
    id=("s",),
)

bad_density_material = change_data(valid_material, mass=5.2)

cases = [
    BasicTestCase(valid_material, None, None, "valid"),
    BasicTestCase(bad_id_material, None, ValidationError, "bad_id"),
    # BasicTestCase(bad_density_material, None, ValueError, "bad_mass"),
]


@pytest.mark.parametrize("tc", cases, ids=case_names(cases))
def test_material(tc: BasicTestCase):
    create_object(tc, Material)
