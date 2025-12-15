from datetime import date
from pydantic import BaseModel


class QResume(BaseModel):
    name: str
    description: str
    receive_date: date