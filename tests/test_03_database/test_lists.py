import pytest
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.database.lists import ListNotFoundExeption
from app.database.lists import ListObject
from app.database.lists import create_new_list_object_in_database
from app.database.lists import delete_list_object_from_database
from app.database.lists import select_all_list_objects
from app.database.lists import select_list_object_by_id
from app.database.lists import update_list_object_in_database


def test_list_not_found_exception() -> None:
    with pytest.raises(ListNotFoundExeption):
        raise ListNotFoundExeption(list_id=str(1))


def test_create_new_list_object_in_database(
    database_session: sessionmaker[Session],
) -> None:
    with database_session.begin() as session:
        new_id = create_new_list_object_in_database(session=session, name="test")
        assert isinstance(new_id, int)


def test_select_list_object_by_id(database_session: sessionmaker[Session]) -> None:
    with database_session.begin() as session:
        list_obj = select_list_object_by_id(session=session, list_id=1)
        assert isinstance(list_obj, ListObject)
        assert isinstance(list_obj.id, int)
        assert list_obj.id == 1


def test_select_all_list_objects(database_session: sessionmaker[Session]) -> None:
    with database_session.begin() as session:
        list_objs = select_all_list_objects(session=session)
        if list_objs is None:
            raise ValueError(
                "Excpected list objects to be in database from earlier test cases"
            )
        assert isinstance(list_objs, list)
        for list_object in list_objs:
            assert isinstance(list_object, ListObject)
            assert isinstance(list_object.id, int)


def test_update_list_object_in_database(
    database_session: sessionmaker[Session],
) -> None:
    with database_session.begin() as session:
        all_list_objects = select_all_list_objects(session=session)
        if all_list_objects is None:
            raise ValueError(
                "Excpected list objects to be in database from earlier test cases"
            )
        list_object = all_list_objects[0]
        list_object_id = list_object.id
        list_object.name = "test new name"
        list_object.sections = "1,2,3"
        update_list_object_in_database(session=session, list_object=list_object)
        retrieved_list_object = select_list_object_by_id(
            session=session, list_id=list_object_id
        )
        if retrieved_list_object is None:
            raise ValueError(
                "Excpected list objects to be in database from earlier test cases"
            )
        assert retrieved_list_object.name == "test new name"
        assert retrieved_list_object.sections == "1,2,3"


def test_delete_list_object_from_database(
    database_session: sessionmaker[Session],
) -> None:
    with database_session.begin() as session:
        all_list_objects = select_all_list_objects(session=session)
        if all_list_objects is None:
            raise ValueError(
                "Excpected list objects to be in database from earlier test cases"
            )
        first_list_object = all_list_objects[0]
        # delete existing list
        delete_list_object_from_database(session=session, list_id=first_list_object.id)

        # store for later use (check if list is deleted in another session)
        first_list_object_id = first_list_object.id

        # delete non existing list
        with pytest.raises(ListNotFoundExeption):
            delete_list_object_from_database(session=session, list_id=123123123123)

    # check if list is deleted, new session is needed
    # as the first session commits when the session closes
    with database_session.begin() as session:
        with pytest.raises(ListNotFoundExeption):
            delete_list_object_from_database(
                session=session, list_id=first_list_object_id
            )


# def test_insert_section_id_to_list_object() -> None:
#     list_object = select_list_object_by_id(1)
#     list_object = insert_section_id_to_list_object(list_object, section_id=4, index=1)
#     assert list_object.sections == "1,4,2,3"


# def test_remove_section_id_from_list_object() -> None:
#     list_object = select_list_object_by_id(1)
#     list_object = remove_section_id_from_list_object(list_object, section_id=4)


# def test_insert_section_id_to_list_object_in_database() -> None:
#     list_object = select_list_object_by_id(1)
#     list_object = insert_section_id_to_list_object_in_database(
#         list_object, section_id=4, index=1
#     )
#     retrieved_list_object = select_list_object_by_id(1)
#     assert retrieved_list_object.sections == "1,4,2,3"


# def test_remove_section_id_from_list_object_in_database() -> None:
#     list_object = select_list_object_by_id(1)
#     assert list_object.sections == "1,4,2,3"
#     list_object = remove_section_id_from_list_object_in_database(
#         list_object, section_id=4
#     )
#     assert list_object.sections == "1,2,3"

#     retrieved_list_object = select_list_object_by_id(1)
#     assert retrieved_list_object.sections == "1,2,3"
