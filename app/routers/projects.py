import json
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

import app.database.projects as projects_engine
from app.models.utils import new_alchemy_encoder

router = APIRouter()


@router.get("/projects")
def get_projects(only_active: bool = True) -> List[str]:
    rows = projects_engine.get_projects(only_active=only_active)
    return [
        json.dumps(
            c,
            cls=new_alchemy_encoder(False, ["id", "name", "active"]),
            check_circular=False,
        )
        for c in rows
    ]


class Project(BaseModel):
    name: str


@router.post("/project")
def create_project(project: Project) -> None:
    projects_engine.add_project(name=project.name)


class PatchProject(BaseModel):
    name: str
    active: bool


@router.patch("/project/{project_id}")
def patch_project(project_id: int, project: PatchProject) -> None:
    projects_engine.patch_project(
        id=project_id, name=project.name, active=project.active
    )


class DeleteProject(BaseModel):
    id: int


@router.delete("/project")
def delete_project(project: DeleteProject) -> None:
    projects_engine.deactivate_project(id=project.id)
