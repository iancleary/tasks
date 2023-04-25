import pytest
from sqlalchemy.orm import Session


@pytest.fixture()
def database_session() -> Session:
    from app.database.core import get_session

    database_session = get_session()
    return database_session
