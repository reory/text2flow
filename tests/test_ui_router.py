"""Unit and integration tests targeting the web UI presentation router."""

from unittest.mock import MagicMock
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
import pytest  # noqa
from app.routers.ui import router, get_templates


def test_get_templates_helper_execution():
    """Verify the template retrieval helper correctly extracts assets from app state."""

    mock_request = MagicMock(spec=Request)
    mock_templates = MagicMock()

    # Simulate FastAPI application state bindings
    mock_request.app.state.templates = mock_templates

    # Explicitly call the unused helper function to claim its coverage lines
    result = get_templates(mock_request)
    assert result == mock_templates


def test_editor_endpoint_rendering_stream():
    """
    Verify the root web presentation route invokes
    template factory rendering engines.
    """

    # Build an isolated mini-app instance to safely decouple router mechanics
    test_app = FastAPI()
    test_app.include_router(router)

    # Mock template responses to completely avoid needing physical HTML files
    mock_templates = MagicMock()
    mock_templates.TemplateResponse.return_value = "mocked_html_markup_payload"
    test_app.state.templates = mock_templates

    client = TestClient(test_app)
    response = client.get("/")

    # Assert successful network transmission states
    assert response.status_code == 200
    assert response.text == '"mocked_html_markup_payload"'

    # Verify the underlying rendering pipeline was triggered with correct configurations
    mock_templates.TemplateResponse.assert_called_once()
    _, kwargs = mock_templates.TemplateResponse.call_args
    assert kwargs["name"] == "editor.html"
    assert kwargs["context"] == {}
