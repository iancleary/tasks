import app.database as database
import app.models.projects as projects


def create_tables() -> None:
    print(database.ENGINE)
    projects.Base.metadata.create_all(database.ENGINE)
