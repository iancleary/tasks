import app.database
from app.models import BASE


def create_tables() -> None:
    engine = app.database.get_database_engine()
    BASE.metadata.create_all(engine)
