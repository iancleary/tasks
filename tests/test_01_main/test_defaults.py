from fastapi import FastAPI

from app.main import app

from app.main import allow_credentials
from app.main import allow_headers
from app.main import allow_methods
from app.main import allow_origins


def test_app() -> None:
    assert isinstance(app, FastAPI)


def test_allow_credentials() -> None:
    assert allow_credentials is True


def test_allow_headers() -> None:
    assert allow_headers == ["Access-Control-Allow-Origin"]


def test_allow_methods() -> None:
    assert allow_methods == ["*"]


def test_allow_origins() -> None:
    assert allow_origins == [
        "http://localhost",
        "http://localhost:3000",
    ]
