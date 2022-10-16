import datetime
import sqlite3


from sqlalchemy import Table, Column, Integer, String, Real

from sqlalchemy import create_engine, sessionmaker

from .models import Base, Movie

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
engine = create_engine("sqlite+pysqlite:///data/data.db", echo=True, future=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def create_tables():
    Base.metadata.create_all(engine)

from sqlalchemy import insert

def add_movie(title:str, release_timestamp:float):
    stmt = insert(Movie).values(title=title, release_timestamp=release_timestamp)
    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()

def get_movies(upcoming:bool=False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,)) # needs to be a tuple
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        return cursor.fetchall()

def watch_movie(title:str):
    with connection:
        connection.execute(SET_MOVIE_WATCHED, (title,))

def get_watched_movies():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES)
        return cursor.fetchall()
