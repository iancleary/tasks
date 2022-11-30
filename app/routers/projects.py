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
            cls=new_alchemy_encoder(False, ["id", "number", "name", "active"]),
            check_circular=False,
        )
        for c in projects
    ]


@router.get("/project/{project_id}")
def get_project(db: Session = Depends(get_db), *, project_id: str) -> str:
    project = db.query(Project).get(project_id)
    return json.dumps(
        project,
        cls=new_alchemy_encoder(False, ["id", "number", "name", "active"]),
        check_circular=False,
    )


class NewProject(BaseModel):
    name: str


@router.post("/project")
def create_project(db: Session = Depends(get_db), *, project: NewProject) -> str:
    project = Project(name=project.name)
    db.add(project)


class PatchProject(BaseModel):
    name: str
    active: bool


@router.patch("/project/{project_id}")
def patch_project(
    db: Session = Depends(get_db), *, project_id: str, project: PatchProject
) -> None:
    project = db.query(Project).get(project_id)

    # column = getattr(Project, "id")
    stmt = (
        update(Project)
        .where(Project.id == project_id)
        .values(name=project.name, active=int(project.active))
    )

    db.execute(stmt)


@router.delete("/project/{project_id}")
def delete_project(db: Session = Depends(get_db), *, project_id: int) -> None:
    column = getattr(Project, "id")
    stmt = update(Project).where(column == project_id).values(active=0)
    db.execute(stmt)
