import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models.projects as projects


DATABASE = os.getenv("DATABASE", "/data/data.db")
engine = create_engine(f"sqlite:///{DATABASE}", echo=True, future=True)
Session = sessionmaker(engine)


def create_tables() -> None:
    print(engine)
    projects.Base.metadata.create_all(engine)

def get_session() -> None:
    return Session