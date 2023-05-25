from typing import List
from typing import Union

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.models.lists import ListObject
from app.models.utils.columns import StrListConverter


class ListNotFoundExeption(Exception):
    def __init__(self, list_id: str):
        self.list_id = list_id

    def __str__(self) -> str:
        return f"List with id {self.list_id} not found."


def create_new_list_object_in_database(
    *, session: Session, name: str  # keyword arguments only
) -> int:
    stmt = insert(ListObject).values(name=name)
    new_list_object_iterator = session.execute(stmt)
    # https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#executing-the-statement
    new_list_object_id = new_list_object_iterator.inserted_primary_key[0]
    return new_list_object_id


def select_list_object_by_id(
    *, session: Session, list_id: int  # keyword arguments only
) -> Union[ListObject, None]:
    obj = session.execute(
        select(ListObject).where(ListObject.id == list_id)
    ).scalar_one_or_none()
    return obj


def select_all_list_objects(
    *, session: Session  # keyword arguments only
) -> Union[List[ListObject], None]:
    iterator_result = session.scalars(select(ListObject))
    # all_rows = [x for x in iterator_result]
    # all_list_objects = [x[0] for x in all_rows]
    # considalte the above two lines into one line (faster)
    all_list_objects = [x for x in iterator_result]
    return all_list_objects


def update_list_object_in_database(*, session: Session, list_object: ListObject) -> str:
    stmt = update(ListObject)
    stmt = stmt.values(
        {
            "id": list_object.id,
            "name": list_object.name,
            "sections": list_object.sections,
        }
    )
    stmt = stmt.where(ListObject.id == list_object.id)
    stmt = stmt.returning(ListObject.name)
    updated_list_obj_iterator = session.execute(stmt)
    updated_list_obj_name = updated_list_obj_iterator.scalar_one()
    return updated_list_obj_name


def delete_list_object_from_database(*, session: Session, list_id: int) -> None:
    list_obj = select_list_object_by_id(session=session, list_id=list_id)

    if list_obj is None:
        raise ListNotFoundExeption(list_id=str(list_id))

    session.delete(list_obj)


def insert_section_id_to_list_object(
    *, list_object: ListObject, section_id: int, index: int  # keyword arguments only
) -> ListObject:
    section_list = StrListConverter.get_list_from_str(list_object.sections)
    section_list[index:index] = [section_id]
    list_object.sections = StrListConverter.make_str_from_list(section_list)
    return list_object


def remove_section_id_from_list_object(
    *, list_object: ListObject, section_id: int  # keyword arguments only
) -> ListObject:
    # this assumes there are no duplicates in sections string
    section_list = StrListConverter.get_list_from_str(list_object.sections)
    section_list.remove(section_id)
    list_object.sections = StrListConverter.make_str_from_list(section_list)
    return list_object


def insert_section_id_to_list_object_in_database(
    *,  # keyword arguments only
    session: Session,
    list_id: int,
    section_id: int,
    index: int,
) -> None:
    list_obj = select_list_object_by_id(session=session, list_id=list_id)

    if list_obj is None:
        raise ListNotFoundExeption(list_id=str(list_id))
    else:
        list_obj = insert_section_id_to_list_object(
            list_object=list_obj, section_id=section_id, index=index
        )

    update_list_object_in_database(session=session, list_object=list_obj)


def remove_section_id_from_list_object_in_database(
    *, session: Session, list_id: int, section_id: int  # keyword arguments only
) -> None:
    list_obj = select_list_object_by_id(session=session, list_id=list_id)

    if list_obj is None:
        raise ListNotFoundExeption(list_id=str(list_id))
    else:
        list_obj = remove_section_id_from_list_object(
            list_object=list_obj, section_id=section_id
        )

    update_list_object_in_database(session=session, list_object=list_obj)
