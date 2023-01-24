import datetime
from enum import IntEnum

from pydantic import BaseModel
from sqlalchemy import REAL
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.models import BASE


class Status(IntEnum):
    BACKLOG = 0
    READY_FOR_WORK = 1
    IN_PROGRESS = 2
    COMPLETED = 3


class Active(IntEnum):
    NO = 0
    YES = 1


class Pinned(IntEnum):
    NO = 0
    YES = 1


# mypy: ignore-errors
class Item(BASE):
    __tablename__ = "items"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    description = Column(String, default="")
    created_date = Column(REAL)
    resolution_date = Column(REAL, default=None)
    status = Column(Integer, default=Status.BACKLOG)
    active = Column(Integer, default=Active.YES)
    pinned = Column(Integer, default=Pinned.NO)

    def __init__(
        self,
        name: str,
        created_date: float = None,
        active: int = None,
        pinned: int = None,
    ) -> None:
        self.name = name
        if created_date is None:
            self.created_date = datetime.datetime.today().timestamp()
        else:
            self.created_date = created_date

        if active is None:
            self.active = Active.YES
        else:
            self.active = active

        if pinned is None:
            self.pinned = Pinned.NO
        else:
            self.pinned = pinned


class PydanticItem(BaseModel):
    id: int
    name: str
    created_date: float
    description: str = ""
    resolution_date: float = None
    status: int = Status.BACKLOG
    active: int = Active.YES
    pinned: int = Pinned.NO
