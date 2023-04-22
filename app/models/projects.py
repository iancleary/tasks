from pydantic import BaseModel
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import Integer
from sqlalchemy import String

from app.models import Base


# mypy: ignore-errors
class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    active: Mapped[int] = mapped_column(Integer, default=1)

    def __init__(self, name: str) -> None:
        self.name = name


class PydanticProject(BaseModel):
    id: int
    name: str
    active: int = 1
