from typing import Union
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.items import Item


def get_item_by_id(db: Session, item_id: Union[int, str]) -> Union[Item, None]:
    if isinstance(item_id, str):
        item_id = int(item_id)
    item = db.execute(select(Item).filter(Item.id == item_id)).scalar_one_or_none()
    return item
