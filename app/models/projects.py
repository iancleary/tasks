from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# mypy: ignore-errors
class Project(Base):
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
