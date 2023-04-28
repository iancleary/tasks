from typing import List
from typing import Union

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.models.items import ItemObject


class ItemNotFoundException(Exception):
    def __init__(self, item_id: str):
        self.item_id = item_id

    def __str__(self) -> str:
        return f"List with id {self.item_id} not found."


def create_new_item_object_in_database(
    *, session: Session, name: str  # keyword arguments only
) -> int:
    new_item_object = ItemObject(name=name)

    new_item_object_iterator = session.execute(
        insert(ItemObject).returning(ItemObject.id),
        {
            "name": new_item_object.name,
            "created_timestamp": new_item_object.created_timestamp,
        },
    )
    new_item_object_id = new_item_object_iterator.scalar_one()
    return new_item_object_id


def select_item_object_by_id(
    *, session: Session, item_id: int  # keyword arguments only
) -> Union[ItemObject, None]:
    obj = session.execute(
        select(ItemObject).where(ItemObject.id == item_id)
    ).scalar_one_or_none()
    return obj


def select_all_item_objects(
    *, session: Session  # keyword arguments only
) -> Union[List[ItemObject], None]:
    iterator_result = session.scalars(select(ItemObject))
    # all_rows = [x for x in iterator_result]
    # all_item_objects = [x[0] for x in all_rows]
    # considalte the above two lines into one line (faster)
    all_item_objects = [x for x in iterator_result]
    return all_item_objects


def update_item_object_in_database(
    *, session: Session, item_object: ItemObject
) -> None:
    stmt = update(ItemObject)
    stmt = stmt.values(
        {
            "id": item_object.id,
            "name": item_object.name,
            "created_timestamp": item_object.created_timestamp,
            "resolution_timestamp": item_object.resolution_timestamp,
            "deleted_timestamp": item_object.deleted_timestamp,
            "description": item_object.resolution_timestamp,
            "status": item_object.status,
            "active": item_object.active,
        }
    )
    stmt = stmt.where(ItemObject.id == item_object.id)
    session.execute(stmt)


def delete_item_object_from_database(*, session: Session, item_id: int) -> None:
    item_obj = select_item_object_by_id(session=session, item_id=item_id)

    if item_obj is None:
        raise ItemNotFoundException(item_id=str(item_id))

    session.delete(item_obj)
