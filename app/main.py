# import datetime
import json
from typing import List

from fastapi import FastAPI

from app.database import projects
from app.database import tables
from app.models.utils import new_alchemy_encoder

app = FastAPI()

tables.create_tables()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/projects")
def get_projects(only_active: bool = True) -> List[str]:
    rows = projects.get_projects(only_active=only_active)
    return [
        json.dumps(
            c,
            cls=new_alchemy_encoder(False, ["id", "name", "active"]),
            check_circular=False,
        )
        for c in rows
    ]


@app.put("/project")
def add_project(name: str) -> None:
    projects.add_project(name=name)


@app.patch("/project")
def patch_project(id: int, name: str, active: bool) -> None:
    projects.patch_project(id=id, name=name, active=active)


@app.delete("/project")
def delete_project(id: int) -> None:
    projects.deactivate_project(id=id)


if __name__ == "__main__":
    import os

    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 80))

    uvicorn.run(app, host=host, port=port, log_level="info")
