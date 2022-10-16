from sqlalchemy import Column, Integer, String, Time, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    title = Column(String, primary_key=True)
    release_timestamp = Column(Float)
    watched = Column(Integer)
    
    def __init__(self, title, release_timestamp, watched=0):

        self.title = title
        self.release_timestamp = release_timestamp
        self.watched = watched

    def to_dict(self):
        return {
            "title": self.title,
            "released_timestamp": self.release_timestamp,
            "watched": self.watched
        }