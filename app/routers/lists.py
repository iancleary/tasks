from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.lists import select_all_list_objects
from app.database.lists import select_list_object_by_id
from app.routers.session import DatabaseSession
from app.schemas import ListObject as ListSchema

router = APIRouter()


@router.get("/all")
def get_items(  # type:ignore
    db: Session = DatabaseSession, response_model=list[ListSchema]
):
    items = select_all_list_objects(session=db)
    if items is None:
        raise HTTPException(status_code=404, detail="No lists found")

    # Fastapi converts from ListObject to ListSchema
    return items


@router.get("/{list_id}")
def get_list(  # type:ignore
    list_id: int, db: Session = DatabaseSession, response_model=ListSchema
):
    list = select_list_object_by_id(session=db, list_id=list_id)
    if list is None:
        raise HTTPException(status_code=404, detail="List not found")

    return list
