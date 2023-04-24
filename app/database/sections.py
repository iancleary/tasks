from typing import Union

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.models.sections import SectionList
from app.models.utils.columns import StrListConverter


class SectionNotFoundExeption(Exception):
    def __init__(self, section_list_id: str):
        self.section_list_id = section_list_id

    def __str__(self) -> str:
        return f"Section list with id {self.section_list_id} not found."


def create_new_section_list_object_in_database(
    db: Session, name: str, list_id: int
) -> None:
    section_list_obj = SectionList(name=name, list_id=list_id)
    db.add(section_list_obj)
    db.commit()


def select_section_list_obj_by_id(db: Session, id: int) -> Union[SectionList, None]:
    obj = db.execute(
        select(SectionList).where(SectionList.id == id)
    ).scalar_one_or_none()
    return obj


def update_section_list_object_in_database(
    db: Session, section_list_object: SectionList
) -> None:
    stmt = update(SectionList)
    stmt = stmt.values(
        {
            "id": section_list_object.id,
            "name": section_list_object.name,
            "items": section_list_object.items,
            "list_id": section_list_object.list_id,
        }
    )
    stmt = stmt.where(SectionList.id == section_list_object.id)
    db.execute(stmt)


def delete_section_list_object_from_database(db: Session, section_list_id: int) -> None:
    section_list_obj = select_section_list_obj_by_id(db, section_list_id)
    db.delete(section_list_obj)
    db.commit()


def add_item_id_to_section_list_object(
    section_list_object: SectionList, item_id: int
) -> SectionList:
    section_list = StrListConverter.get_list_from_str(section_list_object.items)
    section_list.add(item_id)
    section_list_object.items = StrListConverter.make_str_from_list(section_list)
    return section_list_object


def remove_item_id_from_section_list_object(
    section_list_object: SectionList, item_id: int
) -> SectionList:
    section_list = StrListConverter.get_list_from_str(section_list_object.items)
    section_list.remove(item_id)
    section_list_object.items = StrListConverter.make_str_from_list(section_list)
    return section_list_object


def add_item_id_to_section_list_in_database(
    db: Session, section_list_id: int, item_id: int
) -> None:
    section_list_obj = select_section_list_obj_by_id(db, section_list_id)

    if section_list_obj is None:
        raise SectionNotFoundExeption(section_list_id=section_list_id)
    else:
        section_list_obj = add_item_id_to_section_list_object(section_list_obj, item_id)

    update_section_list_object_in_database(db, section_list_obj)


def remove_item_id_from_section_list_in_database(
    db: Session, section_list_id: int, item_id: int
) -> None:
    section_list_obj = select_section_list_obj_by_id(db, section_list_id)

    if section_list_obj is None:
        raise SectionNotFoundExeption(section_list_id=section_list_id)
    else:
        section_list_obj = remove_item_id_from_section_list_object(
            section_list_obj, item_id
        )

    update_section_list_object_in_database(db, section_list_obj)
