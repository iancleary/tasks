import pytest
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker


@pytest.fixture()
def database_session() -> sessionmaker[Session]:
    from app.database.core import get_session

    database_session = get_session()
    return database_session
