import datetime

from sqlalchemy import create_engine
from sqlalchemy import insert, select, update
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import Session

# Pick one feature that will be useful for users
# and then go about implementing it in the simplest way possible

# title, release_date, watched

# CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
#     title TEXT,
#     release_timestamp REAL,
#     watched INTEGER
# );"""

# INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp, watched) VALUES (?, ?, 0);" # good practice to include columns, leave empty does all
# SELECT_ALL_MOVIES = "SELECT * FROM movies;"
# SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;" # number of seconds since 1st of January 1970 right now
# SELECT_WATCHED_MOVIES = "SELECT * FROM movies WHERE watched = 1;"
# SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?;"



# connection = sqlite3.connect("/data/data.db")
# need 4 slashes (https://docs.sqlalchemy.org/en/13/core/engines.html#sqlite)
engine = create_engine('sqlite:////data/data.db', echo=True, future=True)
Session = sessionmaker(engine)
import models

def create_tables():    
    print(engine)
    models.Base.metadata.create_all(engine)

def add_movie(title:str, release_timestamp:float):
    with Session.begin() as session:
        doesn't handle if it's not a unique title
        movie = models.Movie(title=title, release_timestamp=release_timestamp)
        session.add_all([movie])

def get_movies(upcoming:bool=False):
    session = Session()
    if upcoming == True:
        today_timestamp = datetime.datetime.today().timestamp()
        stmt = select(models.Movie).where(models.Movie.c.release_timestamp >= today_timestamp)
    else:
        stmt = select(models.Movie)
    return session.scalars(stmt)


def watch_movie(title:str):
    with engine.connect() as conn:
        stmt = update(models.Movie).where(models.Movie.c.title == title).values(watched = 1)
        conn.execute(stmt)

def get_watched_movies():
    with engine.connect() as conn:
        stmt = select(models.Movie).where(models.Movie.c.watched == 1)
        return conn.execute(stmt)
