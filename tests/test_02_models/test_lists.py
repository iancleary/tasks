from pydantic import BaseModel

from app.models.lists import ListObject
from app.models.lists import PydanticItemList


def test_pydantic_item_list() -> None:
    example_pydantic_item_list = PydanticItemList(
        id=1,
        name="test",
        sections="1,2,3",
    )
    assert isinstance(example_pydantic_item_list, PydanticItemList)
    assert isinstance(example_pydantic_item_list, BaseModel)


def test_list_object_defaults() -> None:
    list_object = ListObject()
    assert isinstance(list_object, ListObject)


def test_list_object_custom_parameters() -> None:
    list_object = ListObject(name="test", sections="1,2,3")
    assert isinstance(list_object, ListObject)
    assert list_object.name == "test"
    assert list_object.sections == "1,2,3"
    assert list_object.id is None
    # list_object.id is not set yet as it is not committed to the database
