from fastapi.routing import APIRoute

from app.main import app


def test_routes() -> None:
    routes = app.routes
    api_routes = [x for x in routes if isinstance(x, APIRoute)]
    # Filter out non-api (fastapi created) routes
    api_route_paths = [(x.path, x.methods) for x in api_routes]

    assert api_route_paths == [
        ("/lists/", {"POST"}),
        ("/lists/all", {"GET"}),
        ("/lists/{list_id}", {"GET"}),
        ("/lists/{list_id}", {"PATCH"}),
        ("/lists/{list_id}", {"DELETE"}),
        ("/health", {"GET"}),
    ]
