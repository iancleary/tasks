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
from app.models.items import UNSET_DATE
from app.models.items import convert_utc_to_local
from app.models.priority import Priority
from app.models.priority import PydanticPriority
from app.models.priority import get_list_from_str
from app.models.priority import make_str_from_list

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

    # Remove item from priority list
    priority = db.query(Priority).first()

    if priority is None:
        priority = Priority(list="")
        db.add(priority)

        # not in priority list, nothing to do
        return

    priority_list = get_list_from_str(priority.list)

    if len(priority_list) == 0:
        # not in priority list, nothing to do
        return

    # Remove from list
    priority_list.remove(int(item_id))
    priority_list_str = make_str_from_list(priority_list)

    priority = db.query(Priority).first()

    stmt = update(Priority)
    stmt = stmt.values({"list": priority_list_str})
    stmt = stmt.where(Priority.id == priority.id)
    db.execute(stmt)


##~ Pinned


@router.patch("/item/{item_id}/priority/yes")
def patch_item_pinned_yes(db: Session = Depends(get_db), *, item_id: str) -> None:
    item = db.query(Item).get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    priority = db.query(Priority).first()

    if priority is None:
        priority = Priority(list=item_id)
        db.add(priority)
        return

    priority_list = get_list_from_str(priority.list)

    # add item to front of list
    priority_list = [int(item_id)] + priority_list

    priority_list_str = make_str_from_list(priority_list)

    priority = db.query(Priority).first()

    stmt = update(Priority)
    stmt = stmt.values({"list": priority_list_str})
    stmt = stmt.where(Priority.id == priority.id)
    db.execute(stmt)


@router.patch("/item/{item_id}/priority/no")
def patch_item_pinned_no(db: Session = Depends(get_db), *, item_id: str) -> None:
    item = db.query(Item).get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    priority = db.query(Priority).first()

    if priority is None:
        priority = Priority(list="")
        db.add(priority)

        # not in priority list, nothing to do
        return

    priority_list = get_list_from_str(priority.list)

    if len(priority_list) == 0:
        # not in priority list, nothing to do
        return

    # Remove from list
    priority_list.remove(int(item_id))
    priority_list_str = make_str_from_list(priority_list)

    priority = db.query(Priority).first()

    stmt = update(Priority)
    stmt = stmt.values({"list": priority_list_str})
    stmt = stmt.where(Priority.id == priority.id)
    db.execute(stmt)


##~ Order


@router.patch("/item/{item_id}/priority/increase")
def increase_item_order(db: Session = Depends(get_db), *, item_id: str) -> None:
    item = db.query(Item).get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    priority = db.query(Priority).first()

    if priority is None:
        priority = Priority(list="")
        db.add(priority)
        priority = db.query(Priority).first()

    priority_list = get_list_from_str(priority.list)

    current_position = priority_list.index(item.id)

    # closer to front of list is higher priority
    desired_position = current_position - 1

    # if item exists at higher priority, swap their positions
    if 0 <= desired_position < len(priority_list):
        a = current_position
        b = desired_position
        priority_list[b], priority_list[a] = priority_list[a], priority_list[b]
    else:
        raise HTTPException(
            status_code=409,
            detail=f"Item {item.id} is the highest priorty, won't increase.",
        )

    priority_list_str = make_str_from_list(priority_list)

    priority = db.query(Priority).first()

    stmt = update(Priority)
    stmt = stmt.values({"list": priority_list_str})
    stmt = stmt.where(Priority.id == priority.id)
    db.execute(stmt)


@router.patch("/item/{item_id}/priority/decrease")
def decrease_item_order(db: Session = Depends(get_db), *, item_id: str) -> None:
    item = db.query(Item).get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    priority = db.query(Priority).first()

    if priority is None:
        priority = Priority(list="")
        db.add(priority)

    priority_list = get_list_from_str(priority.list)

    current_position = priority_list.index(item.id)

    # closer to back of list is lower priority
    desired_position = current_position + 1

    # if item exists at lower priority, swap their positions
    if 0 <= desired_position < len(priority_list):
        a = current_position
        b = desired_position
        priority_list[b], priority_list[a] = priority_list[a], priority_list[b]
    else:
        raise HTTPException(
            status_code=409,
            detail=f"Item {item.id} is the lowest priorty, won't decrease.",
        )

    priority_list_str = make_str_from_list(priority_list)

    priority = db.query(Priority).first()

    stmt = update(Priority)
    stmt = stmt.values({"list": priority_list_str})
    stmt = stmt.where(Priority.id == priority.id)
    db.execute(stmt)


@router.get("/items/priority/")
def get_priority_items(db: Session = Depends(get_db)) -> List[PydanticItem]:

    priority = db.query(Priority).first()

    if priority is None:
        priority = Priority(list="")
        db.add(priority)
        return []

    priority_object = PydanticPriority(**jsonable_encoder(priority))
    priority_list = get_list_from_str(priority_object.list)

    if len(priority_list) == 0:
        # not in priority list, nothing to get
        return []

    items = db.query(Item).filter(Item.id.in_(priority_list))

    json_compatible_return_data = [jsonable_encoder(x) for x in items]

    # make a dictionary so I can lookup by id when sorting
    json_dict = {x["id"]: x for x in json_compatible_return_data}

    # sort list to match priority list
    json_compatible_return_data = [json_dict[y] for y in priority_list]

    # convert to json, then correct timezone on dict-like object,
    # then instantiate return type for validation
    json_compatible_return_data = [
        convert_utc_to_local(x) for x in json_compatible_return_data
    ]
    return [PydanticItem(**x) for x in json_compatible_return_data]
