from typing import List

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy import select

from app.database import Database
from app.models.projects import Project
from app.models.projects import PydanticProject

router = APIRouter()


##~~ Create
class ProjectName(BaseModel):
    name: str


@router.post("/project")
def create_project(db: Database, *, project: ProjectName) -> None:
    project_to_add_to_db = Project(name=project.name)
    db.add(project_to_add_to_db)


##~~ Read


@router.get("/projects")
def get_projects(db: Database, *, only_active: bool = True) -> List[PydanticProject]:
    if only_active is True:
        projects = db.execute(select(Project).filter_by(active=1)).scalars()
    else:
        projects = db.execute(select(Project)).scalars()

    return [PydanticProject(**jsonable_encoder(c)) for c in projects]


@router.get("/project/{project_id}")
def get_project(db: Database, *, project_id: str) -> PydanticProject:
    project = db.execute(select(Project).filter_by(id=int(project_id))).scalar_one()
    return PydanticProject(**jsonable_encoder(project))


##~~ Update


class NewName(BaseModel):
    name: str


@router.patch("/project/{project_id}")
def patch_project(db: Database, *, project_id: str, updates: NewName) -> None:
    # rename project
    stmt = update(Project)
    stmt = stmt.values({"name": updates.name})
    stmt = stmt.where(Project.id == project_id)
    db.execute(stmt)


##~~ Delete


@router.delete("/project/{project_id}")
def delete_project(db: Database, *, project_id: int) -> None:
    # Don't remove row, but deactivate project instead (design choice)
    column = getattr(Project, "id")
    stmt = update(Project).where(column == project_id).values(active=0)
    db.execute(stmt)
