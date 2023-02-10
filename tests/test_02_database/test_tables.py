import app.database.tables as tables
from app.models import BASE


def test_create_tables() -> None:
    tables.create_tables()

    metadata = BASE.metadata

    print(f"dir(metadata): {dir(metadata)}")
    print(f"metadata.tables.keys(): {metadata.tables.keys()}")
    assert "projects" in metadata.tables.keys()
    assert "items" in metadata.tables.keys()
    # assert "priority" in metadata.tables.keys()
