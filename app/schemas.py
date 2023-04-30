from typing import Union

from pydantic import BaseModel

from app.models.items import Description


class ItemBase(BaseModel):
    name: str
    description: str = Description.DEFAULT
    section_id: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    created_timestamp: Union[float, None] = None
    # updated_timestamp:  Union[float, None] = None
    completed_timestamp: Union[float, None] = None
    deleted_timestamp: Union[float, None] = None
    is_completed: int = False
    is_deleted: int = False

    class Config:
        orm_mode = True


class SectionBase(BaseModel):
    name: str


class SectionCreate(SectionBase):
    pass


class Section(SectionBase):
    id: int
    list_id: int
    items: list[Item] = []

    class Config:
        orm_mode = True


class ListBase(BaseModel):
    name: str


class ListCreate(ListBase):
    pass


# deconflict with the List object in the Python standard library typing module
class ListObject(ListBase):
    id: int
    sections: str = ""

    class Config:
        orm_mode = True


class ListUpdate(ListBase):
    id: int
