import json
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.items import Item
from app.models.utils import new_alchemy_encoder

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
def get_items(db: Session = Depends(get_db), *, only_active: bool = True) -> List[str]:
    if only_active is True:
        items = db.query(Item).filter(Item.status == 1)
    else:
        items = db.query(Item)

    return [
        json.dumps(
            c,
            cls=new_alchemy_encoder(False, ["id", "name", "active"]),
            check_circular=False,
        )
        for c in items
    ]


@router.get("/item/{item_id}")
def get_item(db: Session = Depends(get_db), *, item_id: str) -> str:
    item = db.query(Item).get(item_id)
    return json.dumps(
        item,
        cls=new_alchemy_encoder(False, ["id", "name", "active"]),
        check_circular=False,
    )


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


##~~ Delete


@router.delete("/item/{item_id}")
def delete_item(db: Session = Depends(get_db), *, item_id: int) -> None:
    # Don't remove row, but deactivate item instead (design choice)
    column = getattr(Item, "id")
    stmt = update(Item).where(column == item_id).values(status=0)
    db.execute(stmt)
