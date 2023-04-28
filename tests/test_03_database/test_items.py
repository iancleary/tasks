import pytest
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.database.items import ItemNotFoundException
from app.database.items import ItemObject
from app.database.items import create_new_item_object_in_database
from app.database.items import delete_item_object_from_database
from app.database.items import select_all_item_objects
from app.database.items import select_item_object_by_id
from app.database.items import update_item_object_in_database


def test_item_not_found_exception() -> None:
    with pytest.raises(ItemNotFoundException):
        raise ItemNotFoundException(item_id=str(1))


def test_create_new_item_object_in_database(
    database_session: sessionmaker[Session],
) -> None:
    with database_session.begin() as session:
        new_id = create_new_item_object_in_database(session=session, name="test item")
        assert isinstance(new_id, int)


def test_select_item_object_by_id(database_session: sessionmaker[Session]) -> None:
    with database_session.begin() as session:
        item_obj = select_item_object_by_id(session=session, item_id=1)
        assert isinstance(item_obj, ItemObject)
        assert isinstance(item_obj.id, int)
        assert item_obj.id == 1


def test_select_all_item_objects(database_session: sessionmaker[Session]) -> None:
    with database_session.begin() as session:
        item_objs = select_all_item_objects(session=session)
        if item_objs is None:
            raise ValueError(
                "Excpected list objects to be in database from earlier test cases"
            )
        assert isinstance(item_objs, list)
        for item_object in item_objs:
            assert isinstance(item_object, ItemObject)
            assert isinstance(item_object.id, int)
            assert isinstance(item_object.created_timestamp, float)


def test_update_item_object_in_database(
    database_session: sessionmaker[Session],
) -> None:
    with database_session.begin() as session:
        all_item_objects = select_all_item_objects(session=session)
        if all_item_objects is None:
            raise ValueError(
                "Excpected list objects to be in database from earlier test cases"
            )
        item_object = all_item_objects[0]
        item_object_id = item_object.id
        item_object.name = "test item new name"
        update_item_object_in_database(session=session, item_object=item_object)
        retrieved_item_object = select_item_object_by_id(
            session=session, item_id=item_object_id
        )
        if retrieved_item_object is None:
            raise ValueError(
                "Excpected list objects to be in database from earlier test cases"
            )
        assert retrieved_item_object.name == "test item new name"


def test_delete_item_object_from_database(
    database_session: sessionmaker[Session],
) -> None:
    with database_session.begin() as session:
        all_item_objects = select_all_item_objects(session=session)
        if all_item_objects is None:
            raise ValueError(
                "Excpected list objects to be in database from earlier test cases"
            )
        first_item_object = all_item_objects[0]
        # delete existing list
        delete_item_object_from_database(session=session, item_id=first_item_object.id)

        # store for later use (check if list is deleted in another session)
        first_item_object_id = first_item_object.id

        # delete non existing list
        with pytest.raises(ItemNotFoundException):
            delete_item_object_from_database(session=session, item_id=123123123123)

    # check if list is deleted, new session is needed
    # as the first session commits when the session closes
    with database_session.begin() as session:
        with pytest.raises(ItemNotFoundException):
            delete_item_object_from_database(
                session=session, item_id=first_item_object_id
            )
