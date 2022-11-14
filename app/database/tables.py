import os

from sqlalchemy import create_engine
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
import app.models.projects as projects


def create_tables() -> None:
    print(engine)
    projects.Base.metadata.create_all(engine)
