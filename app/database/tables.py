import app.models.projects as projects
from app.database import ENGINE


def create_tables() -> None:
    print(ENGINE)
    projects.Base.metadata.create_all(ENGINE)
