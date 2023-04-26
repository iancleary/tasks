import pytest
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.database.sections import SectionNotFoundExeption
from app.database.sections import SectionObject
from app.database.sections import create_new_section_object_in_database
from app.database.sections import delete_section_object_from_database
from app.database.sections import select_all_section_objects
from app.database.sections import select_section_object_by_id
from app.database.sections import update_section_object_in_database


def test_list_not_found_exception() -> None:
    with pytest.raises(SectionNotFoundExeption):
        raise SectionNotFoundExeption(section_id=str(1))


def test_create_new_section_object_in_database(
    database_session: sessionmaker[Session],
) -> None:
    with database_session.begin() as session:
        new_id = create_new_section_object_in_database(session=session, name="test")
        assert isinstance(new_id, int)


def test_select_section_object_by_id(database_session: sessionmaker[Session]) -> None:
    with database_session.begin() as session:
        section_obj = select_section_object_by_id(session=session, section_id=1)
        assert isinstance(section_obj, SectionObject)
        assert isinstance(section_obj.id, int)
        assert section_obj.id == 1


def test_select_all_section_objects(database_session: sessionmaker[Session]) -> None:
    with database_session.begin() as session:
        section_objs = select_all_section_objects(session=session)
        if section_objs is None:
            raise ValueError(
                "Excpected list objects to be in database from earlier test cases"
            )
        assert isinstance(section_objs, list)
        for section_object in section_objs:
            assert isinstance(section_object, SectionObject)
            assert isinstance(section_object.id, int)


def test_update_section_object_in_database(
    database_session: sessionmaker[Session],
) -> None:
    with database_session.begin() as session:
        all_section_objects = select_all_section_objects(session=session)
        if all_section_objects is None:
            raise ValueError(
                "Excpected list objects to be in database from earlier test cases"
            )
        section_object = all_section_objects[0]
        section_object_id = section_object.id
        section_object.name = "test new name"
        section_object.items = "1,2,3"
        update_section_object_in_database(
            session=session, section_object=section_object
        )
        retrieved_section_object = select_section_object_by_id(
            session=session, section_id=section_object_id
        )
        if retrieved_section_object is None:
            raise ValueError(
                "Excpected list objects to be in database from earlier test cases"
            )
        assert retrieved_section_object.name == "test new name"
        assert retrieved_section_object.items == "1,2,3"


def test_delete_section_object_from_database(
    database_session: sessionmaker[Session],
) -> None:
    with database_session.begin() as session:
        all_section_objects = select_all_section_objects(session=session)
        if all_section_objects is None:
            raise ValueError(
                "Excpected list objects to be in database from earlier test cases"
            )
        first_section_object = all_section_objects[0]
        # delete existing list
        delete_section_object_from_database(
            session=session, section_id=first_section_object.id
        )

        # store for later use (check if list is deleted in another session)
        first_section_object_id = first_section_object.id

        # delete non existing list
        with pytest.raises(SectionNotFoundExeption):
            delete_section_object_from_database(
                session=session, section_id=123123123123
            )

    # check if list is deleted, new session is needed
    # as the first session commits when the session closes
    with database_session.begin() as session:
        with pytest.raises(SectionNotFoundExeption):
            delete_section_object_from_database(
                session=session, section_id=first_section_object_id
            )


# def test_insert_section_id_to_section_object() -> None:
#     section_object = select_section_object_by_id(1)
#     section_object = insert_section_id_to_section_object(
#       section_object, section_id=4, index=1
#     )
#     assert section_object.sections == "1,4,2,3"


# def test_remove_section_id_from_section_object() -> None:
#     section_object = select_section_object_by_id(1)
#     section_object = remove_section_id_from_section_object(
#       section_object, section_id=4
#     )


# def test_insert_section_id_to_section_object_in_database() -> None:
#     section_object = select_section_object_by_id(1)
#     section_object = insert_section_id_to_section_object_in_database(
#         section_object, section_id=4, index=1
#     )
#     retrieved_section_object = select_section_object_by_id(1)
#     assert retrieved_section_object.sections == "1,4,2,3"


# def test_remove_section_id_from_section_object_in_database() -> None:
#     section_object = select_section_object_by_id(1)
#     assert section_object.sections == "1,4,2,3"
#     section_object = remove_section_id_from_section_object_in_database(
#         section_object, section_id=4
#     )
#     assert section_object.sections == "1,2,3"

#     retrieved_section_object = select_section_object_by_id(1)
#     assert retrieved_section_object.sections == "1,2,3"
