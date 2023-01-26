import os
from datetime import datetime

from environs import Env

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.database import tables
from app.routers import items
from app.routers import projects

env = Env()
env.read_env()  # read .env file, if it exists

app = FastAPI()

allow_origins = env.list(
    name="ALLOW_ORIGINS",
    subcast=str,
    default=[
        "http://localhost",  # docs viewing by user
        "http://localhost:3000",  # frontend default
    ],
)

allow_credentials = env.bool(name="ALLOWED_CREDENTIALS", default=True)

allow_methods = env.list(
    name="ALLOWED_METHODS",
    subcast=str,
    default=["*"],
)

allow_headers = env.list(
    name="ALLOWED_HEADERS",
    subcast=str,
    default=["Access-Control-Allow-Origin"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=allow_credentials,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)

app.include_router(projects.router)
app.include_router(items.router)

tables.create_tables()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"msg": "Hello World"}


@app.get("/")
def debug_time() -> dict[str, str]:
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    return {"time": current_time}


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    log_level = os.getenv("LOG_LEVEL", "info")
    uvicorn.run(app, host=host, port=port, log_level=log_level)
