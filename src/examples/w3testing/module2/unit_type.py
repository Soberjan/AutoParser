from pydantic import BaseModel


class UnitType(BaseModel):
    name: str
    velocity: float
