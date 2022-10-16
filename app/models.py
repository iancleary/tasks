from numbers import Real
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Real
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    title = Column(String, primary_key=True)
    release_timestamp = Column(Real)
    watched = Column(Integer)

