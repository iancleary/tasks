from pydantic import BaseModel

from app.models.items import ItemObject
from app.models.items import PydanticItem
from app.models.items import Description
from app.models.items import Active
from app.models.items import Status


def test_pydantic_item_list() -> None:
    example_pydantic_item_list = PydanticItem(
        id=1,
        name="test",
    )
    assert isinstance(example_pydantic_item_list, PydanticItem)
    assert isinstance(example_pydantic_item_list, BaseModel)


def test_list_object_defaults() -> None:
    list_object = ItemObject(name="test")
    assert isinstance(list_object, ItemObject)
    assert list_object.name == "test"
    assert isinstance(list_object.created_date, float)
    assert list_object.resolution_date is None
    assert list_object.deleted_date is None
    assert list_object.status == Status.OPEN
    assert list_object.active == Active.YES
    assert list_object.description == Description.DEFAULT
    assert list_object.id is None
    # list_object.id is not set yet as it is not committed to the database
