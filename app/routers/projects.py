from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.projects import Project
from app.models.projects import PydanticProject

router = APIRouter()


##~~ Create
class NewProject(BaseModel):
    name: str


@router.post("/project")
def create_project(db: Session = Depends(get_db), *, project: NewProject) -> None:
    project = Project(name=project.name)
    db.add(project)


##~~ Read


@router.get("/projects")
def get_projects(
    db: Session = Depends(get_db), *, only_active: bool = True
) -> List[PydanticProject]:
    if only_active is True:
        projects = db.query(Project).filter(Project.active == 1)
    else:
        projects = db.query(Project)

    return [jsonable_encoder(c) for c in projects]


@router.get("/project/{project_id}")
def get_project(db: Session = Depends(get_db), *, project_id: str) -> PydanticProject:
    project = db.query(Project).get(project_id)
    return jsonable_encoder(project)


##~~ Update


class NewName(BaseModel):
    name: str


@router.patch("/project/{project_id}")
def patch_project(
    db: Session = Depends(get_db), *, project_id: str, updates: NewName
) -> None:
    # rename project
    stmt = update(Project)
    stmt = stmt.values({"name": updates.name})
    stmt = stmt.where(Project.id == project_id)
    db.execute(stmt)


##~~ Delete


@router.delete("/project/{project_id}")
def delete_project(db: Session = Depends(get_db), *, project_id: int) -> None:
    # Don't remove row, but deactivate project instead (design choice)
    column = getattr(Project, "id")
    stmt = update(Project).where(column == project_id).values(active=0)
    db.execute(stmt)
