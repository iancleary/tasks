from typing import List
from typing import Union

from sqlalchemy import select

from app.database.core import get_session
from app.models.items import Active
from app.models.items import ItemObject


def select_item_by_id(item_id: Union[int, str]) -> Union[ItemObject, None]:
    if isinstance(item_id, str):
        item_id = int(item_id)
    database_session = get_session()
    with database_session.begin() as session:
        item = session.execute(
            select(ItemObject).filter(ItemObject.id == item_id)
        ).scalar_one_or_none()
        return item


def select_active_items() -> List[ItemObject]:
    database_session = get_session()
    with database_session.begin() as session:
        items = session.execute(
            select(ItemObject).filter_by(active=Active.YES)
        ).scalars()
        item_objects = [ItemObject(**item) for item in items]
        return item_objects
