import datetime
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.items import Item
from app.models.items import PydanticItem
from app.models.items import Status
from app.models.items import Active
from app.models.items import Pinned
from app.models.items import Order
from app.models.items import UNSET_DATE
from app.models.items import convert_utc_to_local

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
def get_items(db: Session = Depends(get_db)) -> List[PydanticItem]:
    items = db.query(Item).filter(Item.active == Active.YES)
    json_compatible_return_data = [jsonable_encoder(x) for x in items]
    json_compatible_return_data = [
        convert_utc_to_local(x) for x in json_compatible_return_data
    ]
    return [PydanticItem(**x) for x in json_compatible_return_data]


@router.get("/items/completed")
def get_completed_items(db: Session = Depends(get_db)) -> List[PydanticItem]:
    items = db.query(Item).filter(
        and_(Item.status == Status.COMPLETED, Item.active == Active.YES)
    )
    json_compatible_return_data = [jsonable_encoder(x) for x in items]

    # convert to json, then correct timezone on dict-like object,
    # then instantiate return type for validation
    json_compatible_return_data = [
        convert_utc_to_local(x) for x in json_compatible_return_data
    ]
    return [PydanticItem(**x) for x in json_compatible_return_data]


@router.get("/items/open")
def get_open_items(db: Session = Depends(get_db)) -> List[PydanticItem]:
    items = db.query(Item).filter(
        and_(Item.status == Status.OPEN, Item.active == Active.YES)
    )
    json_compatible_return_data = [jsonable_encoder(x) for x in items]

    # convert to json, then correct timezone on dict-like object,
    # then instantiate return type for validation
    json_compatible_return_data = [
        convert_utc_to_local(x) for x in json_compatible_return_data
    ]
    return [PydanticItem(**x) for x in json_compatible_return_data]


@router.get("/items/deleted")
def get_deleted_items(db: Session = Depends(get_db)) -> List[PydanticItem]:
    items = db.query(Item).filter(
        and_(Item.status == Status.OPEN, Item.active == Active.NO)
    )
    json_compatible_return_data = [jsonable_encoder(x) for x in items]

    # convert to json, then correct timezone on dict-like object,
    # then instantiate return type for validation
    json_compatible_return_data = [
        convert_utc_to_local(x) for x in json_compatible_return_data
    ]
    return [PydanticItem(**x) for x in json_compatible_return_data]


@router.get("/item/{item_id}")
def get_item(db: Session = Depends(get_db), *, item_id: str) -> PydanticItem:
    item = db.query(Item).get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    # convert to json, then correct timezone on dict-like object,
    # then instantiate return type for validation
    return PydanticItem(**convert_utc_to_local(jsonable_encoder(item)))


##~~ Update


class ItemPatch(BaseModel):
    name: str
    description: str


@router.patch("/item/{item_id}")
def patch_item(
    db: Session = Depends(get_db), *, item_id: str, updates: ItemPatch
) -> None:
    stmt = update(Item)
    stmt = stmt.where(Item.id == item_id)
    stmt = stmt.values(name=updates.name, description=updates.description)
    db.execute(stmt)


##~~ Delete


@router.delete("/item/{item_id}")
def delete_item(db: Session = Depends(get_db), *, item_id: int) -> None:
    # Don't remove row, but deactivate item instead (design choice)
    column = getattr(Item, "id")

    deleted_timestamp = datetime.datetime.utcnow().timestamp()
    # can't deleted completed item
    stmt = (
        update(Item)
        .where(and_(column == item_id, Item.status != Status.COMPLETED))
        .values({"active": Active.NO, "deleted_date": deleted_timestamp})
    )
    db.execute(stmt)


@router.patch("/item/{item_id}/activate")
def activate_item(db: Session = Depends(get_db), *, item_id: int) -> None:
    column = getattr(Item, "id")
    stmt = (
        update(Item)
        .where(column == item_id)
        .values({"active": Active.YES, "deleted_date": UNSET_DATE})
    )
    db.execute(stmt)


##~ Status


@router.patch("/item/{item_id}/status/open")
def patch_item_status_open(db: Session = Depends(get_db), *, item_id: str) -> None:
    stmt = update(Item)
    stmt = stmt.values(
        {"status": Status.OPEN, "resolution_date": UNSET_DATE, "active": Active.YES}
    )
    stmt = stmt.where(Item.id == item_id)
    db.execute(stmt)


@router.patch("/item/{item_id}/status/completed")
def patch_item_status_completed(db: Session = Depends(get_db), *, item_id: str) -> None:
    stmt = update(Item)
    completed_timestamp = datetime.datetime.utcnow().timestamp()
    stmt = stmt.values(
        {
            "status": Status.COMPLETED,
            "resolution_date": completed_timestamp,
            "active": Active.YES,
        }
    )
    stmt = stmt.where(Item.id == item_id)
    db.execute(stmt)


##~ Pinned


@router.patch("/item/{item_id}/pinned/yes")
def patch_item_pinned_yes(db: Session = Depends(get_db), *, item_id: str) -> None:
    stmt = update(Item)
    stmt = stmt.values({"pinned": Pinned.YES})
    stmt = stmt.where(Item.id == item_id)
    db.execute(stmt)


@router.patch("/item/{item_id}/pinned/no")
def patch_item_pinned_no(db: Session = Depends(get_db), *, item_id: str) -> None:
    stmt = update(Item)
    stmt = stmt.values({"pinned": Pinned.NO, "order_": Order.IGNORE})
    stmt = stmt.where(Item.id == item_id)
    db.execute(stmt)


##~ Order


@router.patch("/item/{item_id}/order/increase")
def increase_item_order(db: Session = Depends(get_db), *, item_id: str) -> None:
    item = db.query(Item).get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    current_order = item.order_
    # prevent increasing past max order (unpin to remove order)
    if current_order == Order.MAX:
        raise HTTPException(
            status_code=409,
            detail=f"Item {item.id} order is already at max of {Order.MAX}",
        )

    if item.pinned == Pinned.NO:
        raise HTTPException(
            status_code=409,
            detail=f"Item {item.id} is not pinned, pin this item",
        )

    new_order = current_order + 1

    update_list = []
    update_list.append({"id": item.id, "order_": new_order})

    # get item to swap
    items = db.query(Item).filter(
        and_(
            Item.status == Status.OPEN,
            Item.active == Active.YES,
            Item.pinned == Pinned.YES,
            Item.order_ == item.order_ + 1,
        )
    )
    json_items = [jsonable_encoder(x) for x in items]

    if len(json_items) == 1:
        item_to_swap_with = PydanticItem(**jsonable_encoder(items[0]))
        update_list.append({"id": item_to_swap_with.id, "order_": current_order})

    db.bulk_update_mappings(Item, update_list)


@router.patch("/item/{item_id}/order/decrease")
def decrease_item_order(db: Session = Depends(get_db), *, item_id: str) -> None:
    item = db.query(Item).get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    current_order = item.order_
    # prevent decreasing past min order (unpin to remove order)
    if current_order == Order.MIN:
        raise HTTPException(
            status_code=409,
            detail=f"Item {item.id} order is already at min of {Order.MIN}.",
        )

    if item.pinned == Pinned.NO:
        raise HTTPException(
            status_code=409,
            detail=f"Item {item.id} is not pinned, pin this item",
        )

    new_order = current_order - 1

    update_list = []
    update_list.append({"id": item.id, "order_": new_order})

    # get item to swap
    items = db.query(Item).filter(
        and_(
            Item.status == Status.OPEN,
            Item.active == Active.YES,
            Item.pinned == Pinned.YES,
            Item.order_ == item.order_ - 1,
        )
    )
    json_items = [jsonable_encoder(x) for x in items]

    if len(json_items) == 1:
        item_to_swap_with = PydanticItem(**jsonable_encoder(items[0]))
        update_list.append({"id": item_to_swap_with.id, "order_": current_order})

    db.bulk_update_mappings(Item, update_list)
