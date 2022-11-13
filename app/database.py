import os
from typing import Any

from sqlalchemy import create_engine, select, update
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.orm import Session, sessionmaker

# Pick one feature that will be useful for users
# and then go about implementing it in the simplest way possible

# name, release_date, watched

# CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS projects (
#     name TEXT,
#     release_timestamp REAL,
#     watched INTEGER
# );"""

# INSERT_MOVIES = "INSERT INTO projects (name, release_timestamp, watched) VALUES (?, ?, 0);" # good practice to include columns, leave empty does all
# SELECT_ALL_MOVIES = "SELECT * FROM projects;"
# SELECT_UPCOMING_MOVIES = "SELECT * FROM projects WHERE release_timestamp > ?;" # number of seconds since 1st of January 1970 right now
# SELECT_WATCHED_MOVIES = "SELECT * FROM projects WHERE watched = 1;"
# SET_MOVIE_WATCHED = "UPDATE projects SET watched = 1 WHERE name = ?;"


# connection = sqlite3.connect("/data/data.db")
# need 4 slashes (https://docs.sqlalchemy.org/en/13/core/engines.html#sqlite)

# Create engine based upon venv or docker volue

DATABASE = os.getenv("DATABASE", "/data/data.db")
engine = create_engine(f"sqlite:///{DATABASE}", echo=True, future=True)
Session = sessionmaker(engine)
import models


def create_tables() -> None:
    print(engine)
    models.Base.metadata.create_all(engine)


def add_project(name: str) -> None:
    with Session.begin() as session:
        project = models.Project(name=name)
        session.add_all([project])


def get_projects(only_active: bool = True) -> ScalarResult[Any]:
    session = Session()
    if only_active == True:
        column = getattr(models.Project, "active")
        stmt = select(models.Project).where(column == 1)
    else:
        stmt = select(models.Project)
    return session.scalars(stmt)


def activate_project(id: int) -> None:
    with Session.begin() as session:
        column = getattr(models.Project, "id")
        stmt = update(models.Project).where(column == id).values(active=1)
        session.execute(stmt)


def deactivate_project(id: int) -> None:
    with Session.begin() as session:
        column = getattr(models.Project, "id")
        stmt = update(models.Project).where(column == id).values(active=0)
        session.execute(stmt)


def patch_project(id: int, name: str, active: bool) -> None:
    with Session.begin() as session:
        column = getattr(models.Project, "id")
        stmt = (
            update(models.Project).where(column == id).values(name=name, active=active)
        )
        session.execute(stmt)


def delete_project(id: int) -> None:
    # don't allow deletion, only deactivations
    deactivate_project(id=id)
