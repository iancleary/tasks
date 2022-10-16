# import datetime
import json
# from typing import Union

import database

from fastapi import FastAPI

app = FastAPI()

database.create_tables()

from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/projects")
def get_projects(active:bool = True):
    rows = database.get_projects(active=active)
    return [json.dumps(c, cls=AlchemyEncoder) for c in rows]

@app.put("/project")
def add_project(name: str):
    database.add_project(name=name)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80, log_level="info")
