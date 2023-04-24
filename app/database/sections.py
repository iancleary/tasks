from typing import Union

from sqlalchemy import select
from sqlalchemy import update

from app.database.core import get_session
from app.models.sections import SectionObject
from app.models.utils.columns import StrListConverter


class SectionNotFoundExeption(Exception):
    def __init__(self, section_list_id: str):
        self.section_list_id = section_list_id

    def __str__(self) -> str:
        return f"Section list with id {self.section_list_id} not found."


def create_new_section_list_object_in_database(name: str, list_id: int) -> None:
    section_list_obj = SectionObject(name=name, list_id=list_id)
    database_session = get_session()
    with database_session.begin() as session:
        session.add(section_list_obj)


def select_section_list_obj_by_id(id: int) -> Union[SectionObject, None]:
    database_session = get_session()
    with database_session.begin() as session:
        obj = session.execute(
            select(SectionObject).where(SectionObject.id == id)
        ).scalar_one_or_none()
        return obj


def update_section_list_object_in_database(section_list_object: SectionObject) -> None:
    database_session = get_session()
    stmt = update(SectionObject)
    stmt = stmt.values(
        {
            "id": section_list_object.id,
            "name": section_list_object.name,
            "items": section_list_object.items,
            "list_id": section_list_object.list_id,
        }
    )
    stmt = stmt.where(SectionObject.id == section_list_object.id)
    with database_session.begin() as session:
        session.execute(stmt)


def delete_section_list_object_from_database(section_list_id: int) -> None:
    section_list_obj = select_section_list_obj_by_id(section_list_id)
    database_session = get_session()
    with database_session.begin() as session:
        session.delete(section_list_obj)


def insert_item_id_to_section_list_object(
    section_list_object: SectionObject, item_id: int, index: int
) -> SectionObject:
    # convert string to list
    section_list = StrListConverter.get_list_from_str(section_list_object.items)
    # insert item_id at index
    section_list[index:index] = [item_id]
    # convert list to string
    section_list_object.items = StrListConverter.make_str_from_list(section_list)
    return section_list_object


def remove_item_id_from_section_list_object(
    section_list_object: SectionObject, item_id: int
) -> SectionObject:
    section_list = StrListConverter.get_list_from_str(section_list_object.items)
    section_list.remove(item_id)
    section_list_object.items = StrListConverter.make_str_from_list(section_list)
    return section_list_object


def add_item_id_to_section_list_in_database(
    section_list_id: int, item_id: int, index: int
) -> None:
    section_list_obj = select_section_list_obj_by_id(section_list_id)

    if section_list_obj is None:
        raise SectionNotFoundExeption(section_list_id=str(section_list_id))
    else:
        section_list_obj = insert_item_id_to_section_list_object(
            section_list_object=section_list_obj, item_id=item_id, index=index
        )
        update_section_list_object_in_database(section_list_object=section_list_obj)


def remove_item_id_from_section_list_in_database(
    section_list_id: int, item_id: int
) -> None:
    section_list_obj = select_section_list_obj_by_id(section_list_id)

    if section_list_obj is None:
        raise SectionNotFoundExeption(section_list_id=str(section_list_id))
    else:
        section_list_obj = remove_item_id_from_section_list_object(
            section_list_obj, item_id
        )

    update_section_list_object_in_database(section_list_obj)
