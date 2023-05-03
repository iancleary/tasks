# Dependency
from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.core import SESSION


def get_db() -> Generator[Session, None, None]:
    database_session = SESSION()
    try:
        yield database_session
    finally:
        database_session.close()


DatabaseSession = Depends(get_db)
