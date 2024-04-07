from fastapi import APIRouter
import app.src.controllers.settings as settings_controller


def test_router_type():
    assert type(settings_controller.settings_router) is APIRouter
    assert settings_controller.settings_router.prefix == '/settings'
    assert len(settings_controller.settings_router.tags) > 0
