from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from typing import List

from app.models import BASE

MAX_LENGTH = 6


# mypy: ignore-errors
class Priority(BASE):
    __tablename__ = "priority"
    id = Column(Integer, autoincrement=True, primary_key=True)
    list = Column(String)

    def __init__(self, list: str = None) -> None:
        self.list = list


class PydanticPriority(BaseModel):
    id: int
    list: str


def get_list_from_str(list_str: str):
    if len(list_str) == 0:
        return []
    if list_str == "":
        return []
    if list_str == "":
        return []
    if list_str is None:
        return []

    split_list = list_str.split(",")

    list_object = []
    for x in split_list:
        if x:
            list_object.append(int(x))
        else:
            pass
    return list_object


def make_str_from_list(list_object: List[int]):
    list_str = ""
    for x in list_object:
        list_str = list_str + "," + str(x)
    return list_str
