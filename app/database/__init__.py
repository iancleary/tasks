import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE = os.getenv("DATABASE", "/data/data.db")
ENGINE = create_engine(f"sqlite:///{DATABASE}", echo=True, future=True)
SESSION = sessionmaker(ENGINE)
