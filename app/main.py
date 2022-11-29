import os
# import datetime

from fastapi import FastAPI
import uvicorn

from app.database import tables
from app.routers import projects

app = FastAPI()
app.include_router(projects.router)

tables.create_tables()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"msg": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
