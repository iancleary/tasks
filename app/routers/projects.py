import json
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.projects import Project
from app.models.utils import new_alchemy_encoder

router = APIRouter()


# class ProjectInput(BaseModel):
#     name: str
#     id: int
#     active: bool


@router.get("/projects")
def get_projects(
    db: Session = Depends(get_db), *, only_active: bool = True
) -> List[str]:
    if only_active == True:
        projects = db.query(Project).filter(Project.active == 1)
    else:
        projects = db.query(Project)

    return [
        json.dumps(
            c,
            cls=new_alchemy_encoder(False, ["id", "name", "active"]),
            check_circular=False,
        )
        for c in projects
    ]


@router.get("/project/{project_id}")
def get_project(db: Session = Depends(get_db), *, project_id: str) -> str:
    project = db.query(Project).get(project_id)
    return json.dumps(
        project,
        cls=new_alchemy_encoder(False, ["id", "name", "active"]),
        check_circular=False,
    )


class NewProject(BaseModel):
    name: str


@router.post("/project")
def create_project(db: Session = Depends(get_db), *, project: NewProject) -> None:
    project = Project(name=project.name)
    db.add(project)


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


@router.delete("/project/{project_id}")
def delete_project(db: Session = Depends(get_db), *, project_id: int) -> None:
    column = getattr(Project, "id")
    stmt = update(Project).where(column == project_id).values(active=0)
    db.execute(stmt)
