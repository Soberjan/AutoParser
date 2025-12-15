from typing import List

from pydantic import BaseModel
from examples.w3testing.module2.material import Material

from examples.w3testing.module2.unit_type import UnitType


class Unit(BaseModel):
    name: str
    type_: UnitType
    content: List[Material]
