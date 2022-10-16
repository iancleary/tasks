# import datetime
import json
# from typing import Union

import database

from fastapi import FastAPI

app = FastAPI()

database.create_tables()

from sqlalchemy.ext.declarative import DeclarativeMeta

# https://stackoverflow.com/a/10664192
def new_alchemy_encoder(revisit_self = False, fields_to_expand = []):
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if revisit_self:
                    if obj in _visited_objs:
                        return None
                    _visited_objs.append(obj)

                # go through each field in this SQLalchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x!='registry']:
                    val = obj.__getattribute__(field)

                    # is this field another SQLalchemy object, or a list of SQLalchemy objects?
                    if isinstance(val.__class__, DeclarativeMeta) or (isinstance(val, list) and len(val) > 0 and isinstance(val[0].__class__, DeclarativeMeta)):
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
def read_root():
    return {"Hello": "World"}


@app.get("/projects")
def get_projects(only_active:bool = True):
    rows = database.get_projects(only_active=only_active)
    return [json.dumps(c, cls=new_alchemy_encoder(False, ['id', 'name', 'active']), check_circular=False) for c in rows]

@app.put("/project")
def add_project(name: str):
    database.add_project(name=name)

@app.patch("/project")
def patch_project(id: int, name:str, active:bool):
    database.update_project(id=id, name=name, active=active)

@app.delete("/project")
def delete_project(id:int):
    database.deactivate_project(id=id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80, log_level="info")
