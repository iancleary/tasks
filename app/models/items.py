import datetime
from enum import IntEnum

from pydantic import BaseModel
from sqlalchemy import REAL
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.models import BASE


# mypy: ignore-errors
class Item(BASE):
    __tablename__ = "items"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    description = Column(String, default="")
    created_date = Column(REAL)
    resolution_date = Column(REAL, default=None)
    status = Column(Integer, default=0)

    def __init__(self, name: str, created_date: float = None) -> None:
        self.name = name
        if created_date is None:
            self.created_date = datetime.datetime.today().timestamp()
        else:
            self.created_date = created_date


class PydanticItem(BaseModel):
    id: int
    name: str
    created_date: float
    description: str = ""
    resolution_date: float = None
    status: int = 1


class Status(IntEnum):
    NOT_YET_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3
