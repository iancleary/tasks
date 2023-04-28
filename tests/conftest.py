import os
import pathlib

from pytest import Config
from pytest import Session

TEST_DATABASE = "data/test.db"  # relative to project root
TEST_DATABASE_URI = f"sqlite:///{TEST_DATABASE}"


def pytest_configure(config: Config) -> None:
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    # Tell application to use test database
    os.environ["DATABASE_URI"] = TEST_DATABASE_URI

    # Delete Test Database File before starting
    TEST_DATABASE_FILE = pathlib.Path(TEST_DATABASE)
    if TEST_DATABASE_FILE.exists():
        TEST_DATABASE_FILE.unlink()

    TEST_DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)


def pytest_sessionstart(session: Session) -> None:
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """

    # Create Tables, such that they are available to all tests
    from sqlalchemy import Table

    import app.database.core.tables as tables
    from app.models import Base
    from app.models.items import ItemObject
    from app.models.lists import ListObject
    from app.models.sections import SectionObject

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


def pytest_sessionfinish(session: Session, exitstatus: int) -> int:
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    return exitstatus


def pytest_unconfigure(config: Config) -> None:
    """
    called before test process is exited.
    """
    # Delete Test Database File
    TEST_DATABASE_FILE = pathlib.Path(TEST_DATABASE)
    if TEST_DATABASE_FILE.exists():
        TEST_DATABASE_FILE.unlink()
