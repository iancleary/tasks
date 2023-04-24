import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.lists import ListNotFoundExeption
from app.database.lists import ListObject
from app.database.lists import create_new_list_object_in_database


def test_list_not_found_exception() -> None:
    with pytest.raises(ListNotFoundExeption):
        raise ListNotFoundExeption(list_id=1)


def test_create_new_list_object_in_database() -> None:
    # an Engine, which the Session will use for connection
    # resources
    engine = create_engine("sqlite:///data/test.db")

    # create session and add objects
    with Session(engine) as session:
        list_obj = ListObject(name="test")
        session.add(list_obj)


def test_create_new_list_object_in_database_function() -> None:
    create_new_list_object_in_database(name="test")
