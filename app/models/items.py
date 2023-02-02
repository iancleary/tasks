import datetime
from enum import IntEnum
from enum import Enum

from pydantic import BaseModel
from sqlalchemy import REAL
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.models import BASE
from app.models.utils import utc_to_local


class Status(IntEnum):
    # These are not ordered...
    # The only thing that matters
    # is that they are unique
    OPEN = 0
    COMPLETED = 1


class Active(IntEnum):
    NO = 0
    YES = 1


class Pinned(IntEnum):
    NO = 0
    YES = 1


class Description(Enum):
    DEFAULT = ""


# This will store as a value of 0.0,
# but code will handle it and massage it to None
#
# Python 3.10.9 (main, Jan 28 2023, 19:03:24) [GCC 9.4.0] on linux
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import datetime
# >>> datetime.datetime.fromtimestamp(0.0)
# datetime.datetime(1969, 12, 31, 17, 0)
#
# Again, code here massages this to None in the Python object
# but the database will store a 0.0
UNSET_DATE = 0.0


# mypy: ignore-errors
class Item(BASE):
    __tablename__ = "items"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    created_date = Column(REAL)
    resolution_date = Column(REAL, default=UNSET_DATE)
    deleted_date = Column(REAL, default=UNSET_DATE)
    status = Column(Integer, default=Status.OPEN)
    active = Column(Integer, default=Active.YES)
    pinned = Column(Integer, default=Pinned.NO)

    def __init__(
        self,
        name: str,
        created_date: float = None,
        resolution_date: float = None,
        deleted_date: float = None,
        description: str = Description.DEFAULT,
        active: int = None,
        pinned: int = None,
    ) -> None:

        self.name = name

        self.description = description

        self.resolution_date = resolution_date

        self.deleted_date = deleted_date

        if created_date is None:
            # store data in UTC.
            #
            # timezone is permitted to be handled by:
            # 1) the client
            # 2) or routes after loading from the database into objects
            #
            # https://docs.python.org/3/library/datetime.html
            #
            # For example (on the morning of January 30th, 2023 in 'US/Arizona'):
            #
            # python3.10
            # >>> import datetime
            # >>> datetime.datetime.now()
            # datetime.datetime(2023, 1, 30, 9, 19, 50, 418246)
            # >>> datetime.datetime.now().timestamp()
            # 1675095596.624964
            # >>> datetime.datetime.utcnow()
            # datetime.datetime(2023, 1, 30, 16, 20, 42, 714811)
            # >>> datetime.datetime.utcnow().timestamp()
            # 1675121142.531571
            #
            self.created_date = datetime.datetime.utcnow().timestamp()
        else:
            self.created_date = datetime.datetime.fromtimestamp(self.created_date)

        if self.resolution_date is None:
            self.resolution_date = None
        else:
            self.resolution_date = datetime.datetime.fromtimestamp(self.resolution_date)

        if self.deleted_date is None:
            self.deleted_date = None
        else:
            self.deleted_date = datetime.datetime.fromtimestamp(self.deleted_date)
        # also need to defined behavior for columns created after the database
        # even though they have default values in the application code,
        # they might not have a value in a new database column,
        # so we must handle these cases below

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
    created_date: datetime.datetime = None
    description: str = ""
    resolution_date: datetime.datetime = None
    deleted_date: datetime.datetime = None
    status: int = Status.OPEN
    active: int = Active.YES
    pinned: int = Pinned.NO


def convert_utc_to_local(item: dict):
    if item is None:
        return item
    if item["created_date"] is not None:
        item["created_date"] = datetime.datetime.fromtimestamp(item["created_date"])
        item["created_date"] = utc_to_local(item["created_date"])

    if item["resolution_date"] is not None:
        item["resolution_date"] = datetime.datetime.fromtimestamp(
            item["resolution_date"]
        )
        item["resolution_date"] = utc_to_local(item["resolution_date"])

    if item["deleted_date"] is not None:
        item["deleted_date"] = datetime.datetime.fromtimestamp(item["deleted_date"])
        item["deleted_date"] = utc_to_local(item["deleted_date"])

    return item
