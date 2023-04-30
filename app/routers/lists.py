from typing import Generator

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.core import SESSION
from app.database.lists import select_all_list_objects
from app.schemas import ListObject

router = APIRouter()


# Dependency
def get_db() -> Generator[Session, None, None]:
    db = SESSION()
    try:
        yield db
    finally:
        db.close()


# mypy: ignore-errors
@router.get("/all")
def get_items(db: Session = Depends(get_db), response_model=list[ListObject]):
    items = select_all_list_objects(session=db)
    if items is None:
        raise HTTPException(status_code=404, detail="No lists found")

    # Fastapi converts from ListObject to ListSchema
    return items
