from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.engine.result import ScalarResult

import app.models.projects as models
from app.database import SESSION


def add_project(name: str) -> None:
    with SESSION.begin() as session:
        project = models.Project(name=name)
        session.add_all([project])


def get_projects(only_active: bool = True) -> ScalarResult:
    session = SESSION()
    if only_active == True:
        column = getattr(models.Project, "active")
        stmt = select(models.Project).where(column == 1)
    else:
        stmt = select(models.Project)
    return session.scalars(stmt)


def activate_project(id: int) -> None:
    with SESSION.begin() as session:
        column = getattr(models.Project, "id")
        stmt = update(models.Project).where(column == id).values(active=1)
        session.execute(stmt)


def deactivate_project(id: int) -> None:
    with SESSION.begin() as session:
        column = getattr(models.Project, "id")
        stmt = update(models.Project).where(column == id).values(active=0)
        session.execute(stmt)


def patch_project(id: int, name: str, active: bool) -> None:
    with SESSION.begin() as session:
        column = getattr(models.Project, "id")
        stmt = (
            update(models.Project).where(column == id).values(name=name, active=active)
        )
        session.execute(stmt)


def delete_project(id: int) -> None:
    # don't allow deletion, only deactivations
    deactivate_project(id=id)
