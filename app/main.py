import uvicorn
from fastapi import FastAPI
from fastapi_cors import CORS
from fastapi_cors.env import HOST
from fastapi_cors.env import LOG_LEVEL
from fastapi_cors.env import PORT

import app.database.core.tables as tables
from app.routers.lists import router as lists_router

# from app.routers import items
# from app.routers import projects


app = FastAPI()
app.include_router(lists_router, prefix="/lists", tags=["lists"])

CORS(app=app)

# app.include_router(projects.router)
# app.include_router(items.router)

tables.create_tables()


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, log_level=LOG_LEVEL)
