from sqlalchemy import Table

import app.database.core.tables as tables
from app.models import Base
from app.models.items import ItemObject
from app.models.lists import ListObject
from app.models.sections import SectionObject


def test_create_tables() -> None:
    tables.create_tables()

    metadata = Base.metadata

    assert isinstance(metadata.tables, dict)
    assert isinstance(ItemObject.__table__, Table)
    assert isinstance(ListObject.__table__, Table)
    assert isinstance(SectionObject.__table__, Table)

    print(f"dir(metadata): {dir(metadata)}")
    print(f"metadata.tables.keys(): {metadata.tables.keys()}")

    assert "items" in metadata.tables.keys()
    assert "sections" in metadata.tables.keys()
    assert "lists" in metadata.tables.keys()
