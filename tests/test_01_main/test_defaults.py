from fastapi import FastAPI
from fastapi_cors.env import ALLOW_ORIGINS
from fastapi_cors.env import ALLOWED_CREDENTIALS
from fastapi_cors.env import ALLOWED_HEADERS
from fastapi_cors.env import ALLOWED_METHODS

from app.main import app


def test_app() -> None:
    assert isinstance(app, FastAPI)


def test_allow_credentials() -> None:
    assert ALLOWED_CREDENTIALS is True


def test_allow_headers() -> None:
    assert ALLOWED_HEADERS == ["Access-Control-Allow-Origin"]


def test_allow_methods() -> None:
    assert ALLOWED_METHODS == ["*"]


def test_allow_origins() -> None:
    assert ALLOW_ORIGINS == [
        "http://localhost",
        "http://localhost:3000",
    ]
