import os
from functools import lru_cache
from typing import Iterator

from fastapi_restful.session import FastAPISessionMaker
from pydantic import BaseSettings
from sqlalchemy.orm import Session


class DBSettings(BaseSettings):
    """Parses variables from environment on instantiation"""

    database_uri: str = os.getenv(
        "DATABASE", "/data/data.db"
    )  # could break up into scheme, username, password, host, db


def get_db() -> Iterator[Session]:
    """FastAPI dependency that provides a sqlalchemy session"""
    yield from _get_fastapi_sessionmaker().get_db()


@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    """This function could be replaced with a global variable if preferred"""
    database_uri = DBSettings().database_uri
    return FastAPISessionMaker(database_uri)
