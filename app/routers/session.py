# Dependency
from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.core import SESSION


def get_db() -> Generator[Session, None, None]:
    db = SESSION()
    try:
        yield db
    finally:
        db.close()


DatabaseSession = Depends(get_db)
