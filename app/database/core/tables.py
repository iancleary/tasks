import app.database
from app.models import Base


def create_tables() -> None:
    engine = app.database.get_database_engine()
    Base.metadata.create_all(engine)
