from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.engine.result import ScalarResult

import app.models.projects as models
from app.database import SESSION


def add_project(name: str) -> dict:

    session = SESSION()
    project = models.Project(name=name)
    session.add(project)
    session.commit()
    ret = project.id
    session.close()
    # with SESSION.begin() as session:
    #     project = models.Project(name=name)
    #     session.add_all([project])
    return ret


def get_project(id: int) -> models.Project:
    session = SESSION()
    stmt = select(models.Project).where(models.Project.id == id)

    # fetch all the records whose id == id
    records = session.execute(stmt).fetchall()

    # should be only 1 record
    record = records[0]

    # record is a tuple with the class inside it
    project = record[0]

    return project


def get_projects(only_active: bool = True) -> ScalarResult:
    if only_active == True:
        getattr(models.Project, "active")
        stmt = select(models.Project).where(models.Project == 1)
    else:
        stmt = select(models.Project)
    return SESSION().scalars(stmt)


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
            update(models.Project)
            .where(column == id)
            .values(name=name, active=int(active))
        )
        session.execute(stmt)


def delete_project(id: int) -> None:
    # don't allow deletion, only deactivations
    deactivate_project(id=id)
