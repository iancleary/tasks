import app.database as database
from app.models import BASE


def create_tables() -> None:
    print(database.ENGINE)
    BASE.metadata.create_all(database.ENGINE)
