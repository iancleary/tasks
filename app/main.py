import os
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
HOST = (os.getenv("HOST", "0.0.0.0"),)
PORT = (int(os.getenv("PORT", 8000)),)
LOG_LEVEL = (os.getenv("LOG_LEVEL", "info"),)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "pass",
        "details": {
            "uptime": {
                "time": START_TIME,
            }
        },
        "env": {
            "HOST": HOST,
            "PORT": PORT,
            "LOG_LEVEL": LOG_LEVEL,
            "ALLOW_ORIGINS": ALLOW_ORIGINS,
            "ALLOWED_CREDENTIALS": ALLOWED_CREDENTIALS,
            "ALLOWED_METHODS": ALLOWED_METHODS,
            "ALLOWED_HEADERS": ALLOWED_HEADERS,
        },
    }


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, log_level=LOG_LEVEL)
