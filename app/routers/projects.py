import json
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

import app.database.projects as projects_engine
from app.models.utils import new_alchemy_encoder

router = APIRouter()


class Project(BaseModel):
    name: str
    id: int
    active: bool


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


@router.get("/project/{project_id}")
def get_project(project_id: int) -> str:
    project = projects_engine.get_project(id=project_id)
    return json.dumps(
        project,
        cls=new_alchemy_encoder(False, ["id", "name", "active"]),
        check_circular=False,
    )


class NewProject(BaseModel):
    name: str


@router.post("/project")
def create_project(project: NewProject) -> str:
    id = projects_engine.add_project(name=project.name)
    return json.dumps({"id": id})


class PatchProject(BaseModel):
    name: str
    active: bool


@router.patch("/project/{project_id}")
def patch_project(project_id: int, project: PatchProject) -> None:
    projects_engine.patch_project(
        id=project_id, name=project.name, active=project.active
    )


@router.delete("/project/{project_id}")
def delete_project(project_id: int) -> None:
    projects_engine.deactivate_project(id=project_id)
