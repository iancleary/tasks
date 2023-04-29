import os
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

DATABASE_URI = str(os.getenv("DATABASE_URI"))
# sqlite 3 "sqllite:///{DATABASE_NAME}
# if DATABASE_NAME does not start with "/" it is relative to current working directory
# if DATABASE_NAME does not exist, it will be created
# For example, you likely want the initial "/" in docker,
# but would not want a venv (outside of docker for testing) to have it.

ENGINE = create_engine(DATABASE_URI)
SESSION = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)


# create functions for when you need to use the engine or session directly
@lru_cache()
def get_database_engine() -> Engine:
    return ENGINE


@lru_cache()
def get_session() -> sessionmaker[Session]:
    return SESSION


Database = Annotated[Session, Depends(get_session)]
