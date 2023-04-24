from pydantic import BaseModel

from app.models.sections import PydanticSectionList
from app.models.sections import SectionObject


def test_pydantic_section_list() -> None:
    example_pydantic_section_list = PydanticSectionList(
        id=1,
        name="test",
        items="1,2,3",
        list_id=1,
    )
    assert isinstance(example_pydantic_section_list, PydanticSectionList)
    assert isinstance(example_pydantic_section_list, BaseModel)


def test_section_object_defaults() -> None:
    section_object = SectionObject()
    assert isinstance(section_object, SectionObject)
    assert section_object.name is None
    assert section_object.items is None
    assert section_object.list_id is None
    assert section_object.id is None
    # section_object.id is not set yet as it is not committed to the database


def test_section_object_custom_parameters() -> None:
    section_object = SectionObject(name="test", items="1,2,3", list_id=1)
    assert isinstance(section_object, SectionObject)
    assert section_object.name == "test"
    assert section_object.items == "1,2,3"
    assert section_object.list_id == 1
    assert section_object.id is None
    # section_object.id is not set yet as it is not committed to the database
