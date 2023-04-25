import pytest

from app.database.lists import ListNotFoundExeption
from app.database.lists import ListObject
from app.database.lists import create_new_list_object_in_database
from app.database.lists import delete_list_object_from_database
from app.database.lists import insert_section_id_to_list_object
from app.database.lists import insert_section_id_to_list_object_in_database
from app.database.lists import remove_section_id_from_list_object
from app.database.lists import remove_section_id_from_list_object_in_database
from app.database.lists import select_list_obj_by_id
from app.database.lists import update_list_object_in_database


def test_list_not_found_exception() -> None:
    with pytest.raises(ListNotFoundExeption):
        raise ListNotFoundExeption(list_id=str(1))


def test_create_new_list_object_in_database() -> None:
    create_new_list_object_in_database(name="test")


def test_select_list_obj_by_id() -> None:
    list_obj = select_list_obj_by_id(1)
    assert isinstance(list_obj, ListObject)


def test_update_list_object_in_database() -> None:
    list_object = select_list_obj_by_id(1)
    list_object.name = "test new name"
    list_object.sections = "1,2,3"
    update_list_object_in_database(list_object)
    retrieved_list_object = select_list_obj_by_id(1)
    assert retrieved_list_object.name == "test new name"
    assert retrieved_list_object.sections == "1,2,3"


def test_delete_list_object_from_database() -> None:
    # delete existing list
    delete_list_object_from_database(1)

    # delete non existing list
    with pytest.raises(ListNotFoundExeption):
        delete_list_object_from_database(123123123123)


def test_insert_section_id_to_list_object() -> None:
    list_object = select_list_obj_by_id(1)
    list_object = insert_section_id_to_list_object(list_object, section_id=4, index=1)
    assert list_object.sections == "1,4,2,3"


def test_remove_section_id_from_list_object() -> None:
    list_object = select_list_obj_by_id(1)
    list_object = remove_section_id_from_list_object(list_object, section_id=4)
    assert list_object.sections == "1,2,3"


def test_insert_section_id_to_list_object_in_database() -> None:
    list_object = select_list_obj_by_id(1)
    list_object = insert_section_id_to_list_object_in_database(
        list_object, section_id=4, index=1
    )
    retrieved_list_object = select_list_obj_by_id(1)
    assert retrieved_list_object.sections == "1,4,2,3"


def test_remove_section_id_from_list_object_in_database() -> None:
    list_object = select_list_obj_by_id(1)
    assert list_object.sections == "1,4,2,3"
    list_object = remove_section_id_from_list_object_in_database(
        list_object, section_id=4
    )
    retrieved_list_object = select_list_obj_by_id(1)
    assert retrieved_list_object.sections == "1,2,3"
