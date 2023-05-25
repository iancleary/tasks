from typing import List
from typing import Union

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.models.sections import SectionObject
from app.models.utils.columns import StrListConverter


class SectionNotFoundExeption(Exception):
    def __init__(self, section_id: str):
        self.section_id = section_id

    def __str__(self) -> str:
        return f"Section with id {self.section_id} not found."


def create_new_section_object_in_database(
    *, session: Session, name: str, list_id: int  # keyword arguments only
) -> int:
    stmt = insert(SectionObject).values(name=name, list_id=list_id)
    cursor_result = session.execute(stmt)  # type: ignore
    # https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#executing-the-statement
    new_section_obj_id = cursor_result.inserted_primary_key[0]  # type: ignore
    return new_section_obj_id


def select_section_object_by_id(
    *, session: Session, section_id: int  # keyword arguments only
) -> Union[SectionObject, None]:
    obj = session.execute(
        select(SectionObject).where(SectionObject.id == section_id)
    ).scalar_one_or_none()
    return obj


def select_all_section_objects(
    *, session: Session  # keyword arguments only
) -> Union[List[SectionObject], None]:
    iterator_result = session.scalars(select(SectionObject))
    # all_rows = [x for x in iterator_result]
    # all_section_objects = [x[0] for x in all_rows]
    # considalte the above two lines into one line (faster)
    all_section_objects = [x for x in iterator_result]
    return all_section_objects


def update_section_object_in_database(
    *, session: Session, section_object: SectionObject
) -> None:
    stmt = update(SectionObject)
    stmt = stmt.values(
        {
            "id": section_object.id,
            "name": section_object.name,
            "items": section_object.items,
            "list_id": section_object.list_id,
        }
    )
    stmt = stmt.where(SectionObject.id == section_object.id)
    session.execute(stmt)


def delete_section_object_from_database(*, session: Session, section_id: int) -> None:
    section_object = select_section_object_by_id(session=session, section_id=section_id)

    if section_object is None:
        raise SectionNotFoundExeption(section_id=str(section_id))

    session.delete(section_object)


def insert_item_id_to_section_object(
    *,
    section_object: SectionObject,
    item_id: int,
    index: int,  # keyword arguments only
) -> SectionObject:
    item_list = StrListConverter.get_list_from_str(section_object.items)
    item_list[index:index] = [item_id]
    section_object.items = StrListConverter.make_str_from_list(item_list)
    return section_object


def remove_item_id_from_section_object(
    *, section_object: SectionObject, item_id: int  # keyword arguments only
) -> SectionObject:
    # this assumes there are no duplicates in sections string
    section_list = StrListConverter.get_list_from_str(section_object.items)
    section_list.remove(item_id)
    section_object.items = StrListConverter.make_str_from_list(section_list)
    return section_object


def insert_item_id_to_section_object_in_database(
    *,  # keyword arguments only
    session: Session,
    section_id: int,
    item_id: int,
    index: int,
) -> None:
    section_object = select_section_object_by_id(session=session, section_id=section_id)

    if section_object is None:
        raise SectionNotFoundExeption(section_id=str(section_id))
    else:
        section_object = insert_item_id_to_section_object(
            section_object=section_object, item_id=item_id, index=index
        )

    update_section_object_in_database(session=session, section_object=section_object)


def remove_item_id_from_section_object_in_database(
    *, session: Session, section_id: int, item_id: int  # keyword arguments only
) -> None:
    section_object = select_section_object_by_id(session=session, section_id=section_id)

    if section_object is None:
        raise SectionNotFoundExeption(section_id=str(section_id))
    else:
        section_object = remove_item_id_from_section_object(
            section_object=section_object, item_id=item_id
        )

    update_section_object_in_database(session=session, section_object=section_object)
