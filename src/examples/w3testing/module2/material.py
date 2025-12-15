from pydantic import BaseModel, Field, model_validator


class Material(BaseModel):
    id: str | int
    density: float = Field(gt=0)
    mass: float = Field(ge=0)
    volume: float = Field(gt=0)

    @model_validator(mode="after")
    def mass_match(self) -> "Material":
        if self.density != self.mass / self.volume:
            raise ValueError("Масса не соответствует объёму")
        return self
