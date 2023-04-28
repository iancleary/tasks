import os
from datetime import datetime
from typing import Union

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import app.database.core.tables as tables
from app.env import env

# from app.routers import items
# from app.routers import projects


app = FastAPI()

ALLOW_ORIGINS = env.list(
    name="ALLOW_ORIGINS",
    subcast=str,
    default=[
        "http://localhost",  # docs viewing by user
        "http://localhost:3000",  # frontend default
    ],
)

ALLOWED_CREDENTIALS = env.bool(name="ALLOWED_CREDENTIALS", default=True)

ALLOWED_METHODS = env.list(
    name="ALLOWED_METHODS",
    subcast=str,
    default=["*"],
)

ALLOWED_HEADERS = env.list(
    name="ALLOWED_HEADERS",
    subcast=str,
    default=["Access-Control-Allow-Origin"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=ALLOWED_CREDENTIALS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)

# app.include_router(projects.router)
# app.include_router(items.router)

tables.create_tables()

START_TIME = datetime.utcnow().isoformat()
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")


class PydanticHealthCheck(BaseModel):
    status: str
    details: dict[str, Union[str, int, dict[str, str]]]
    env: dict[str, Union[str, int, list[str]]]


@app.get("/health")
def health_check() -> JSONResponse:
    health_check = PydanticHealthCheck(
        status="pass",
        details={"uptime": {"time": START_TIME}},
        env={
            "HOST": HOST,
            "PORT": PORT,
            "LOG_LEVEL": LOG_LEVEL,
            "ALLOW_ORIGINS": ALLOW_ORIGINS,
            "ALLOWED_CREDENTIALS": ALLOWED_CREDENTIALS,
            "ALLOWED_METHODS": ALLOWED_METHODS,
            "ALLOWED_HEADERS": ALLOWED_HEADERS,
        },
    )
    json_compatible_health_check = jsonable_encoder(health_check)
    return JSONResponse(content=json_compatible_health_check)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, log_level=LOG_LEVEL)
