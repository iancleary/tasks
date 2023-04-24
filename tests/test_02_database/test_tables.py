import app.database.core.tables as tables
from app.models import Base


def test_create_tables() -> None:
    tables.create_tables()

    metadata = Base.metadata

    print(f"dir(metadata): {dir(metadata)}")
    print(f"metadata.tables.keys(): {metadata.tables.keys()}")
    assert "items" in metadata.tables.keys()
    assert "sections" in metadata.tables.keys()
    assert "lists" in metadata.tables.keys()
