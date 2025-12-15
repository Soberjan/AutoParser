from datetime import date
from pydantic import BaseModel


class Resume(BaseModel):
    id: int
    name: str
    receive_date: date

class ResumeItem(BaseModel):
    id: int
    name: str
    description: str
    receive_date: date

