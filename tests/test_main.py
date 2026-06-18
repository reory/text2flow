"""Unit and integration tests targeting the primary FastAPI application lifecycle entry point."""

from fastapi.testclient import TestClient
from fastapi.templating import Jinja2Templates
from app.main import app

client = TestClient(app)


def test_app_initialization_and_metadata():
    """Verify that the FastAPI instance initializes with the correct title metadata."""

    assert app.title == "Text2Flow"


def test_app_state_templates_registration():
    """
    Verify that Jinja2Templates instance
    successfully binds to the global application state.
    """

    assert hasattr(app.state, "templates")
    # Robust check: Validate the type itself to remain version-agnostic
    assert isinstance(app.state.templates, Jinja2Templates)


def test_static_files_mounted():
    """
    Verify that the static files directory is
    correctly mounted to the asset router routing table.
    """

    # Lookup by name, which is more reliable across framework updates
    static_route = next(
        (r for r in app.routes if getattr(r, "name", None) == "static"), None
    )

    assert static_route is not None
    assert static_route.path == "/static"


def test_routers_are_included():
    """
    Verify that additional routers (UI and API) are
    registered beyond the default FastAPI endpoints.
    """

    """
    A default FastAPI app has 4 base routes (docs, openapi json, redoc, etc.) 
    + 1 static mount = 5 total.
    If the UI and API routers were successfully included, 
    the total route count will exceed 5.
    """

    assert len(app.routes) > 5
