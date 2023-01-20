from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.items import Item
from app.models.items import PydanticItem
from app.models.items import Status

router = APIRouter()


##~~ Create
class NewItem(BaseModel):
    name: str


@router.post("/item")
def create_item(db: Session = Depends(get_db), *, item: NewItem) -> None:
    item = Item(name=item.name)
    db.add(item)


##~~ Read


@router.get("/items")
def get_items(
    db: Session = Depends(get_db), *, only_uncomplete_items: bool = True
) -> List[PydanticItem]:
    if only_uncomplete_items is True:
        items = db.query(Item).filter(Item.status != Status.COMPLETED)
    else:
        items = db.query(Item)

    json_compatible_return_data = [jsonable_encoder(x) for x in items]
    return [PydanticItem(**x) for x in json_compatible_return_data]


@router.get("/item/{item_id}")
def get_item(db: Session = Depends(get_db), *, item_id: str) -> PydanticItem:
    item = db.query(Item).get(item_id)
    return PydanticItem(**jsonable_encoder(item))


##~~ Update


class NewName(BaseModel):
    name: str


@router.patch("/item/{item_id}")
def patch_item(
    db: Session = Depends(get_db), *, item_id: str, updates: NewName
) -> None:
    # rename item
    stmt = update(Item)
    stmt = stmt.values({"name": updates.name})
    stmt = stmt.where(Item.id == item_id)
    db.execute(stmt)


@router.patch("/item/{item_id}/not-yet-started")
def patch_item_status_not_yet_started(
    db: Session = Depends(get_db), *, item_id: str
) -> None:
    stmt = update(Item)
    stmt = stmt.values({"status": Status.NOT_YET_STARTED})
    stmt = stmt.where(Item.id == item_id)
    db.execute(stmt)


@router.patch("/item/{item_id}/in-progress")
def patch_item_status_in_progress(
    db: Session = Depends(get_db), *, item_id: str
) -> None:
    stmt = update(Item)
    stmt = stmt.values({"status": Status.IN_PROGRESS})
    stmt = stmt.where(Item.id == item_id)
    db.execute(stmt)


@router.patch("/item/{item_id}/complete")
def patch_item_status_complete(db: Session = Depends(get_db), *, item_id: str) -> None:
    stmt = update(Item)
    stmt = stmt.values({"status": Status.COMPLETED})
    stmt = stmt.where(Item.id == item_id)
    db.execute(stmt)


##~~ Delete


@router.delete("/item/{item_id}")
def delete_item(db: Session = Depends(get_db), *, item_id: int) -> None:
    # Don't remove row, but deactivate item instead (design choice)
    column = getattr(Item, "id")
    stmt = update(Item).where(column == item_id).values(status=0)
    db.execute(stmt)
