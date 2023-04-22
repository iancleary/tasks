import datetime
from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import and_
from sqlalchemy import update
from sqlalchemy import select

from app.database import Database
from app.database.items import get_item_by_id
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
class ItemName(BaseModel):
    name: str


@router.post("/item")
def create_item(db: Database, *, item: ItemName) -> None:
    item_to_add_to_db = Item(name=item.name)
    db.add(item_to_add_to_db)


##~~ Read


@router.get("/items")
def get_items(db: Database) -> List[PydanticItem]:
    items = db.execute(select(Item).filter_by(active=Active.YES)).scalars()
    json_compatible_return_data = [jsonable_encoder(x) for x in items]
    json_compatible_return_data = [
        convert_utc_to_local(x) for x in json_compatible_return_data
    ]
    return [PydanticItem(**x) for x in json_compatible_return_data]


@router.get("/item/focus")
def get_focus_item(db: Database) -> List[PydanticItem]:
    priority = db.execute(select(Priority)).scalar_one_or_none()

    if priority is None:
        priority = Priority(list="")
        db.add(priority)
        return []

    priority_object = PydanticPriority(**jsonable_encoder(priority))
    priority_list = get_list_from_str(priority_object.list)

    if len(priority_list) == 0:
        # not in limited priority list, nothing to get
        return []

    # get first item
    priority_list = [priority_list[0]]

    items = db.query(Item).filter(Item.id.in_(priority_list))

    json_compatible_return_data = [jsonable_encoder(x) for x in items]

    # make a dictionary so I can lookup by id when sorting
    # convert to json, then correct timezone on dict-like object,
    # then instantiate return type for validation
    pydantic_item_by_id = {
        s["id"]: PydanticItem(**convert_utc_to_local(s))
        for s in json_compatible_return_data
    }

    # sort list to match priority list
    sorted_pydantic_items = [pydantic_item_by_id[y] for y in priority_list]

    # convert to json, then correct timezone on dict-like object,
    # then instantiate return type for validation
    return sorted_pydantic_items


@router.get("/items/priority")
def get_priority_items(db: Database) -> List[PydanticItem]:
    priority = db.execute(select(Priority)).scalar_one_or_none()

    if priority is None:
        priority = Priority(list="")
        db.add(priority)
        return []

    priority_object = PydanticPriority(**jsonable_encoder(priority))
    priority_list = get_list_from_str(priority_object.list)

    if len(priority_list) == 0:
        # not in limited priority list, nothing to get
        return []

    items = db.execute(select(Item).filter(Item.id.in_(priority_list))).scalars()

    json_compatible_return_data = [jsonable_encoder(x) for x in items]

    # make a dictionary so I can lookup by id when sorting
    # convert to json, then correct timezone on dict-like object,
    # then instantiate return type for validation
    pydantic_item_by_id = {
        s["id"]: PydanticItem(**convert_utc_to_local(s))
        for s in json_compatible_return_data
    }

    # sort list to match priority list
    sorted_pydantic_items = [pydantic_item_by_id[y] for y in priority_list]

    # convert to json, then correct timezone on dict-like object,
    # then instantiate return type for validation
    return sorted_pydantic_items


@router.get("/items/completed")
def get_completed_items(db: Database) -> List[PydanticItem]:
    items = db.execute(
        select(Item)
        .filter(and_(Item.status == Status.COMPLETED, Item.active == Active.YES))
        .order_by(Item.resolution_date.desc())  # most recent completions first
    ).scalars()
    json_compatible_return_data = [jsonable_encoder(x) for x in items]

    # convert to json, then correct timezone on dict-like object,
    # then instantiate return type for validation
    json_compatible_return_data = [
        convert_utc_to_local(x) for x in json_compatible_return_data
    ]
    return [PydanticItem(**x) for x in json_compatible_return_data]


@router.get("/items/open")
def get_open_items(db: Database) -> List[PydanticItem]:
    items = db.execute(
        select(Item).filter(and_(Item.status == Status.OPEN, Item.active == Active.YES))
    ).scalars()
    json_compatible_return_data = [jsonable_encoder(x) for x in items]

    # convert to json, then correct timezone on dict-like object,
    # then instantiate return type for validation
    json_compatible_return_data = [
        convert_utc_to_local(x) for x in json_compatible_return_data
    ]
    return [PydanticItem(**x) for x in json_compatible_return_data]


@router.get("/items/deleted")
def get_deleted_items(db: Database) -> List[PydanticItem]:
    items = db.execute(
        select(Item).filter(and_(Item.status == Status.OPEN, Item.active == Active.NO))
    ).scalars()
    json_compatible_return_data = [jsonable_encoder(x) for x in items]

    # convert to json, then correct timezone on dict-like object,
    # then instantiate return type for validation
    json_compatible_return_data = [
        convert_utc_to_local(x) for x in json_compatible_return_data
    ]
    return [PydanticItem(**x) for x in json_compatible_return_data]


@router.get("/item/{item_id}")
def get_item(db: Database, *, item_id: str) -> PydanticItem:
    item = get_item_by_id(db, item_id)

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
def patch_item(db: Database, *, item_id: str, updates: ItemPatch) -> None:
    stmt = update(Item)
    stmt = stmt.where(Item.id == item_id)
    stmt = stmt.values(name=updates.name, description=updates.description)
    db.execute(stmt)


##~~ Delete


@router.delete("/item/{item_id}")
def delete_item(db: Database, *, item_id: int) -> None:
    # Don't remove row, but deactivate item instead (design choice)
    column = getattr(Item, "id")

    deleted_timestamp = datetime.datetime.utcnow().timestamp()
    # can't deleted completed item

    item_table = Item.__table__
    stmt = (
        item_table.update()
        .where(and_(column == item_id, Item.status != Status.COMPLETED))
        .values({"active": Active.NO, "deleted_date": deleted_timestamp})
    )
    db.execute(stmt)

    # Remove item from priority list
    priority = db.execute(select(Priority)).scalar_one_or_none()

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

    priority = db.execute(select(Priority)).scalar_one_or_none()

    if priority is not None:
        stmt = update(Priority)
        stmt = stmt.values({"list": priority_list_str})
        stmt = stmt.where(Priority.id == priority.id)
        db.execute(stmt)


@router.patch("/item/{item_id}/activate")
def activate_item(db: Database, *, item_id: int) -> None:
    column = getattr(Item, "id")
    item_table = Item.__table__
    stmt = (
        item_table.update()
        .where(column == item_id)
        .values({"active": Active.YES, "deleted_date": UNSET_DATE})
    )
    db.execute(stmt)


##~ Status


@router.patch("/item/{item_id}/status/open")
def patch_item_status_open(db: Database, *, item_id: str) -> None:
    item_table = Item.__table__
    stmt = item_table.update()
    stmt = stmt.values(
        {"status": Status.OPEN, "resolution_date": UNSET_DATE, "active": Active.YES}
    )
    stmt = stmt.where(Item.id == item_id)
    db.execute(stmt)


@router.patch("/item/{item_id}/status/completed")
def patch_item_status_completed(db: Database, *, item_id: str) -> None:
    item_table = Item.__table__
    stmt = item_table.update()
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
    priority = db.execute(select(Priority)).scalar_one_or_none()

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

    priority = db.execute(select(Priority)).scalar_one_or_none()

    if priority is not None:
        stmt = update(Priority)
        stmt = stmt.values({"list": priority_list_str})
        stmt = stmt.where(Priority.id == priority.id)
        db.execute(stmt)


##~ Pinned


@router.patch("/item/{item_id}/priority/yes")
def patch_item_priority_yes(db: Database, *, item_id: str) -> None:
    item_table = Item.__table__
    stmt = item_table.update()
    item = db.query(Item).get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    priority = db.execute(select(Priority)).scalar_one_or_none()

    if priority is None:
        priority = Priority(list=item_id)
        db.add(priority)
        return

    priority_list = get_list_from_str(priority.list)

    item_id_int = int(item_id)

    if item_id_int in priority_list:
        raise HTTPException(
            status_code=409,
            detail=f"Item {item.id} is already in the priority list.",
        )

    # add item to back of list
    priority_list = priority_list + [item_id_int]

    priority_list_str = make_str_from_list(priority_list)

    priority = db.execute(select(Priority)).scalar_one_or_none()

    if priority is not None:
        stmt = update(Priority)
        stmt = stmt.values({"list": priority_list_str})
        stmt = stmt.where(Priority.id == priority.id)
        db.execute(stmt)


@router.patch("/item/{item_id}/priority/no")
def patch_item_priority_no(db: Database, *, item_id: str) -> None:
    item = db.query(Item).get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    priority = db.execute(select(Priority)).scalar_one_or_none()

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

    priority = db.execute(select(Priority)).scalar_one_or_none()

    if priority is not None:
        stmt = update(Priority)
        stmt = stmt.values({"list": priority_list_str})
        stmt = stmt.where(Priority.id == priority.id)
        db.execute(stmt)


##~ Order


@router.patch("/item/{item_id}/priority/increase")
def increase_item_order(db: Database, *, item_id: str) -> None:
    item = db.query(Item).get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    priority = db.execute(select(Priority)).scalar_one_or_none()

    if priority is None:
        priority = Priority(list="")
        db.add(priority)
        priority = db.execute(select(Priority)).scalar_one_or_none()

    if priority is not None:
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

    priority = db.execute(select(Priority)).scalar_one_or_none()

    if priority is not None:
        stmt = update(Priority)
        stmt = stmt.values({"list": priority_list_str})
        stmt = stmt.where(Priority.id == priority.id)
        db.execute(stmt)


@router.patch("/item/{item_id}/priority/decrease")
def decrease_item_order(db: Database, *, item_id: str) -> None:
    item = db.query(Item).get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    priority = db.execute(select(Priority)).scalar_one_or_none()

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

    priority = db.execute(select(Priority)).scalar_one_or_none()

    if priority is not None:
        stmt = update(Priority)
        stmt = stmt.values({"list": priority_list_str})
        stmt = stmt.where(Priority.id == priority.id)
        db.execute(stmt)
