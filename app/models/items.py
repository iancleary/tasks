import datetime
from enum import IntEnum
from enum import StrEnum
from typing import Union

from pydantic import BaseModel
from sqlalchemy import REAL
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models import Base
from app.models.utils.datetime import utc_to_local


class Description(StrEnum):
    DEFAULT = ""


class Status(IntEnum):
    # These are not ordered...
    # The only thing that matters
    # is that they are unique
    OPEN = 0
    COMPLETED = 1


class Active(IntEnum):
    NO = 0
    YES = 1


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
class ItemObject(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    name: Mapped[int] = mapped_column(String)
    created_date: Mapped[float] = mapped_column(REAL)
    resolution_date: Mapped[float] = mapped_column(REAL, default=UNSET_DATE)
    deleted_date: Mapped[float] = mapped_column(REAL, default=UNSET_DATE)
    status: Mapped[int] = mapped_column(Integer, default=Status.OPEN)
    active: Mapped[int] = mapped_column(Integer, default=Active.YES)
    description: Mapped[str] = mapped_column(String, default=Description.DEFAULT)

    def __init__(
        self,
        name: str,
        created_date: float = None,
        resolution_date: float = None,
        deleted_date: float = None,
        description: str = "",
        active: int = None,
    ) -> None:
        self.name = name

        self.resolution_date = resolution_date

        self.deleted_date = deleted_date

        if description is None:
            self.description = Description.DEFAULT
        else:
            self.description = description

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


class PydanticItem(BaseModel):
    id: int
    name: Union[str, None]
    created_date: datetime.datetime = None
    description: Union[str, None] = Description.DEFAULT
    resolution_date: datetime.datetime = None
    deleted_date: datetime.datetime = None
    status: int = Status.OPEN
    active: int = Active.YES


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
