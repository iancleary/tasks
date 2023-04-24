from pydantic import BaseModel
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models import Base


class ListObject(Base):
    __tablename__ = "lists"
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    sections: Mapped[str] = mapped_column(String, default="")


class PydanticItemList(BaseModel):
    id: int
    name: str
    sections: str
