from app.models.items import Description
from app.models.items import ItemObject

# from app.models.items import PydanticItem


# def test_pydantic_item() -> None:
#     example_pydantic_item = PydanticItem(
#         id=1,
#         name="test",
#     )
#     assert isinstance(example_pydantic_item, PydanticItem)
#     assert isinstance(example_pydantic_item, BaseModel)


def test_item_object_defaults() -> None:
    list_object = ItemObject(name="test")
    assert isinstance(list_object, ItemObject)
    assert list_object.name == "test"
    assert isinstance(list_object.created_timestamp, float)
    assert list_object.resolution_timestamp is None
    assert list_object.deleted_timestamp is None
    assert list_object.is_open is True
    assert list_object.is_active is True
    assert list_object.description == Description.DEFAULT
    assert list_object.id is None
    # list_object.id is not set yet as it is not committed to the database
    # and the id is set by the database
