import json
from typing import List

from fastapi import APIRouter

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


@router.put("/project")
def add_project(name: str) -> None:
    projects_engine.add_project(name=name)


@router.patch("/project")
def patch_project(id: int, name: str, active: bool) -> None:
    projects_engine.patch_project(id=id, name=name, active=active)


@router.delete("/project")
def delete_project(id: int) -> None:
    projects_engine.deactivate_project(id=id)
