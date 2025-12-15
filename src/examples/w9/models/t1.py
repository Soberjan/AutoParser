from pydantic import BaseModel


class T1(BaseModel):
    id: str
    name: str