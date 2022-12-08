import os
import pathlib

from pytest import Config

TEST_DATABASE = "data/test.db"


def pytest_configure(config: Config) -> None:
    # Tell application to use test database
    os.environ["DATABASE"] = TEST_DATABASE

    # Delete Test Database File before starting
    TEST_DATABASE_FILE = pathlib.Path(TEST_DATABASE)
    if TEST_DATABASE_FILE.exists():
        TEST_DATABASE_FILE.unlink()


def pytest_unconfigure(config: Config) -> None:
    # Delete Test Database File
    TEST_DATABASE_FILE = pathlib.Path(TEST_DATABASE)
    if TEST_DATABASE_FILE.exists():
        TEST_DATABASE_FILE.unlink()
