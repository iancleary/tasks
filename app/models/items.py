from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.models import BASE


# mypy: ignore-errors
class Project(BASE):
    __tablename__ = "projects"
    # id = Column(String, primary_key=True)
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    description = Column(String, default="")
    created_date = Column(Integer)
    resolution_date = Column(Integer)
    status = Column(Integer, default=1)

    def __init__(self, name: str) -> None:
        # if self.id == None:
        #     self.id = str(uuid.uuid4())
        self.name = name

    # def _to_dict(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "active": self.active
    #     }
