# import datetime
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Union

from fastapi import FastAPI

from app.database import projects
from app.database import tables

app = FastAPI()

tables.create_tables()

from sqlalchemy.ext.declarative import DeclarativeMeta


# https://stackoverflow.com/a/10664192
def new_alchemy_encoder(
    revisit_self: bool = False, fields_to_expand: List[str] = []
) -> Any:
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj: object) -> Union[List[str], object]:
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if revisit_self:
                    if obj in _visited_objs:
                        return None
                    _visited_objs.append(obj)

                # go through each field in this SQLalchemy class
                fields: Dict[str, Any] = {}
                for field in [
                    x
                    for x in dir(obj)
                    if not x.startswith("_") and x != "metadata" and x != "registry"
                ]:
                    val = obj.__getattribute__(field)

                    # is this field another SQLalchemy object, or a list of SQLalchemy objects?
                    if isinstance(val.__class__, DeclarativeMeta) or (
                        isinstance(val, list)
                        and len(val) > 0
                        and isinstance(val[0].__class__, DeclarativeMeta)
                    ):
                        # unless we're expanding this field, stop here
                        if field not in fields_to_expand:
                            # not expanding this field: set it to None and continue
                            fields[field] = None
                            continue

                    fields[field] = val
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder


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
