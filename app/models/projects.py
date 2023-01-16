from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.models import BASE


# mypy: ignore-errors
class Project(BASE):
    __tablename__ = "projects"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    active = Column(Integer, default=1)

    def __init__(self, name: str) -> None:
        self.name = name


class PydanticProject(BaseModel):
    id: int
    name: str
    active: int = 1
