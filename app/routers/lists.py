from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.lists import create_new_list_object_in_database
from app.database.lists import select_all_list_objects
from app.database.lists import select_list_object_by_id
from app.database.lists import update_list_object_in_database
from app.routers.session import DatabaseSession
from app.schemas import ListCreate
from app.schemas import ListObject as ListSchema

router = APIRouter()


@router.post("/")
def create_list(  # type:ignore
    list: ListCreate,
    database_session: Session = DatabaseSession,
) -> int:
    with database_session:
        new_list_object_id = create_new_list_object_in_database(
            name=list.name, session=database_session
        )
        database_session.commit()
    return new_list_object_id


@router.get("/all")
def get_items(  # type:ignore
    database_session: Session = DatabaseSession, response_model=list[ListSchema]
):
    items = select_all_list_objects(session=database_session)
    if items is None:
        raise HTTPException(status_code=404, detail="No lists found")

    # Fastapi converts from ListObject to ListSchema
    return items


@router.get("/{list_id}")
def get_list(  # type:ignore
    list_id: int, database_session: Session = DatabaseSession, response_model=ListSchema
):
    list_object = select_list_object_by_id(session=database_session, list_id=list_id)
    if list_object is None:
        raise HTTPException(status_code=404, detail="List not found")

    return list_object


@router.patch("/{list_id}")
def update_list(  # type:ignore
    list: ListCreate,
    list_id: int,
    database_session: Session = DatabaseSession,
) -> str:
    with database_session:
        list_object = select_list_object_by_id(
            session=database_session, list_id=list_id
        )
        if list_object is None:
            raise HTTPException(status_code=404, detail="List not found")

        # update name
        list_object.name = list.name
        updated_list_object_name = update_list_object_in_database(
            session=database_session, list_object=list_object
        )
        database_session.commit()
    return updated_list_object_name
