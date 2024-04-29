from fastapi.routing import APIRoute

from app.main import application

AUTH_ROUTES_COUNT = 4
PROFILE_ROUTES_COUNT = 3
STATUS_ROUTES_COUNT = 1
MATCHING_ROUTES_COUNT = 2
ROUTERS_COUNT = AUTH_ROUTES_COUNT \
    + PROFILE_ROUTES_COUNT \
    + STATUS_ROUTES_COUNT \
    + MATCHING_ROUTES_COUNT


def test_app_routes_count():
    api_routes = list(
        filter(lambda x: type(x) is APIRoute, application.routes)
    )
    assert len(api_routes) == ROUTERS_COUNT
