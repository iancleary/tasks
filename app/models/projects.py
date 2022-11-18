from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.models import BASE


# mypy: ignore-errors
class Project(BASE):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(Integer, default=1)

    def __init__(self, name: str) -> None:
        self.name = name

    # def _to_dict(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "active": self.active
    #     }
