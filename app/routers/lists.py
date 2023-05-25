from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.lists import ListNotFoundExeption
from app.database.lists import create_new_list_object_in_database
from app.database.lists import delete_list_object_from_database
from app.database.lists import select_all_list_objects
from app.database.lists import select_list_object_by_id
from app.database.lists import update_list_object_in_database
from app.models.lists import ListObject
from app.routers.session import DatabaseSession
from app.schemas import ListCreate
from app.schemas import ListObject as ListSchema

router = APIRouter()


@router.post("/", response_model=int)
def create_list(
    list: ListCreate,
    database_session: Session = DatabaseSession,
) -> int:
    with database_session:
        new_list_object_id = create_new_list_object_in_database(
            name=list.name, session=database_session
        )
        database_session.commit()
    return new_list_object_id


@router.get("/all", response_model=list[ListSchema])
def get_items(
    database_session: Session = DatabaseSession,
) -> list[ListObject]:
    items = select_all_list_objects(session=database_session)
    if items is None:
        raise HTTPException(status_code=404, detail="No lists found")

    # Fastapi converts from ListObject to ListSchema
    return items


@router.get("/{list_id}", response_model=ListSchema)
def get_list(list_id: int, database_session: Session = DatabaseSession) -> ListObject:
    list_object = select_list_object_by_id(session=database_session, list_id=list_id)
    if list_object is None:
        raise HTTPException(
            status_code=404, detail=f"List with id {list_id} not found."
        )

    return list_object


@router.patch("/{list_id}", response_model=str)
def update_list(
    list: ListCreate,
    list_id: int,
    database_session: Session = DatabaseSession,
) -> str:
    with database_session:
        list_object = select_list_object_by_id(
            session=database_session, list_id=list_id
        )
        if list_object is None:
            raise HTTPException(
                status_code=404, detail=f"List with id {list_id} not found."
            )

        # update name
        list_object.name = list.name
        updated_list_object_name = update_list_object_in_database(
            session=database_session, list_object=list_object
        )
        database_session.commit()
    return updated_list_object_name


@router.delete("/{list_id}")
def delete_list(
    list_id: int,
    database_session: Session = DatabaseSession,
) -> None:
    with database_session:
        try:
            delete_list_object_from_database(session=database_session, list_id=list_id)
        except Exception as e:
            if type(e) == ListNotFoundExeption:
                raise HTTPException(status_code=404, detail=str(e))
            else:
                raise HTTPException(status_code=500, detail=str(e))
        database_session.commit()
    return None
