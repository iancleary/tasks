from typing import Union
from sqlalchemy import update
from sqlalchemy import select

from sqlalchemy.orm import Session
from app.models.lists import ListObject
from app.models.utils.columns import StrListConverter


class ListNotFoundExeption(Exception):
    def __init__(self, list_id: str):
        self.list_id = list_id

    def __str__(self) -> str:
        return f"List with id {self.list_id} not found."


def create_new_list_object_in_database(db: Session, name: str, list_id: int) -> None:
    list_obj = ListObject(name=name, list_id=list_id)
    db.add(list_obj)
    db.commit()


def select_list_obj_by_id(db: Session, id: int) -> Union[ListObject, None]:
    obj = db.execute(select(ListObject).where(ListObject.id == id)).scalar_one_or_none()
    return obj


def update_list_object_in_database(db: Session, list_object: ListObject) -> None:
    stmt = update(ListObject)
    stmt = stmt.values(
        {
            "id": list_object.id,
            "name": list_object.name,
            "sections": list_object.sections,
        }
    )
    stmt = stmt.where(ListObject.id == list_object.id)
    db.execute(stmt)


def delete_list_object_from_database(db: Session, list_id: int) -> None:
    list_obj = select_list_obj_by_id(db, list_id)
    db.delete(list_obj)
    db.commit()


def add_item_id_to_list_object(list_object: ListObject, item_id: int) -> ListObject:
    sections = StrListConverter.get_list_from_str(list_object.sections)
    sections.add(item_id)
    list_object.sections = StrListConverter.make_str_from_list(list)
    return list_object


def remove_item_id_from_list_object(
    list_object: ListObject, item_id: int
) -> ListObject:
    sections = StrListConverter.get_list_from_str(list_object.sections)
    sections.remove(item_id)
    list_object.sections = StrListConverter.make_str_from_list(list)
    return list_object


def add_item_id_to_list_in_database(db: Session, list_id: int, item_id: int) -> None:
    list_obj = select_list_obj_by_id(db, list_id)

    if list_obj is None:
        raise ListNotFoundExeption(list_id=list_id)
    else:
        list_obj = add_item_id_to_list_object(list_obj, item_id)

    update_list_object_in_database(db, list_obj)


def remove_item_id_from_list_in_database(
    db: Session, list_id: int, item_id: int
) -> None:
    list_obj = select_list_obj_by_id(db, list_id)

    if list_obj is None:
        raise ListNotFoundExeption(list_id=list_id)
    else:
        list_obj = remove_item_id_from_list_object(list_obj, item_id)

    update_list_object_in_database(db, list_obj)
