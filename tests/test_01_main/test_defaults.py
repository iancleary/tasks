import os
import time

from fastapi import FastAPI

from app.main import app

def test_app() -> None:
    assert isinstance(app, FastAPI)
