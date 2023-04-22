from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.items import Item


def get_item_by_id(db: Session, item_id: int):
    item = db.execute(select(Item).filter(Item.id == item_id)).scalar_one_or_none()
    return item
