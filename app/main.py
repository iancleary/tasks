# import datetime

from fastapi import FastAPI

from app.database import tables
from app.routers import projects

app = FastAPI()
app.include_router(projects.router)

tables.create_tables()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"msg": "Hello World"}


if __name__ == "__main__":
    import os

    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 80))

    uvicorn.run(app, host=host, port=port, log_level="info")
