from fastapi.routing import APIRoute

from app.main import app


def test_routes() -> None:
    routes = app.routes
    api_routes = [x for x in routes if isinstance(x, APIRoute)]
    # Filter out non-api (fastapi created) routes
    api_route_paths = [x.path for x in api_routes]

    assert api_route_paths == [
        "/lists/all",
        "/lists/{list_id}",
        "/lists/",
        "/health",
    ]
