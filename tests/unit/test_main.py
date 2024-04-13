from fastapi.routing import APIRoute

from app.main import app

AUTH_ROUTES_COUNT = 4


def test_app_routes_count():
    api_routes = list(filter(lambda x: type(x) is APIRoute, app.routes))
    assert len(api_routes) == AUTH_ROUTES_COUNT
