from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models import Base


class SectionObject(Base):
    __tablename__ = "sections"
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    items: Mapped[str] = mapped_column(String)
    list_id: Mapped[int] = mapped_column(Integer, ForeignKey("lists.id"))


class PydanticSectionList(BaseModel):
    id: int
    name: str
    items: str
    list_id: int
