from app.database.core import get_database_engine
from app.models import Base


def create_tables() -> None:
    engine = get_database_engine()
    Base.metadata.create_all(engine)
    print(f"Database tables: {Base.metadata.tables.keys()}")
