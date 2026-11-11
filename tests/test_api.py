"""Unit tests targeting the FastAPI programmatic endpoints."""

from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routers.api import router

# Create a clean, isolated FastAPI app instance specifically for this test file
app = FastAPI()
app.include_router(router)

# Set raise_server_exceptions=False so TestClient returns 500 HTTP responses
# instead of re-raising unhandled backend exceptions in the test runner.
client = TestClient(app, raise_server_exceptions=False)


@patch("app.routers.api.parse_edges")
@patch("app.routers.api.render_flowchart")
def test_render_diagram_success_png(mock_render, mock_parse):
    """Verify successful rendering of PNG flowcharts returns a 200 status code."""

    mock_parse.return_value = [("A", "B")]
    mock_render.return_value = b"fake_png_binary_bytes"

    payload = {"text": "A -> B", "format": "png"}
    response = client.post("/api/render", json=payload)

    assert response.status_code == 200
    assert response.content == b"fake_png_binary_bytes"
    assert response.headers["content-type"] == "image/png"

    mock_parse.assert_called_once_with("A -> B")
    mock_render.assert_called_once_with([("A", "B")], format="png", engine="dot")


@patch("app.routers.api.parse_edges")
@patch("app.routers.api.render_flowchart")
def test_render_diagram_success_svg(mock_render, mock_parse):
    """Verify alternative media type mapping works correctly for SVG format."""

    mock_parse.return_value = [("X", "Y")]
    mock_render.return_value = b"<svg>mock_vector_data</svg>"

    payload = {"text": "X -> Y", "format": "svg"}
    response = client.post("/api/render", json=payload)

    assert response.status_code == 200
    assert response.content == b"<svg>mock_vector_data</svg>"
    assert response.headers["content-type"] == "image/svg+xml"


@patch("app.routers.api.parse_edges")
def test_render_diagram_validation_error(mock_parse):
    """Verify that a ValueError in parsing returns a 400 Bad Request error response."""

    mock_parse.side_effect = ValueError("Invalid syntax: missing relationship arrow")

    payload = {"text": "Bad Syntax Input Block", "format": "png"}
    response = client.post("/api/render", json=payload)

    assert response.status_code == 400
    assert response.text == "Invalid syntax: missing relationship arrow"


@patch("app.routers.api.parse_edges")
def test_render_diagram_system_error(mock_parse):
    """
    Verify that an unexpected backend exception 
    triggers a 500 Internal Server Error.
    """

    mock_parse.side_effect = Exception("Graphviz binary executable missing on machine environment")

    payload = {"text": "A -> B", "format": "png"}
    response = client.post("/api/render", json=payload)

    assert response.status_code == 500
    assert response.status_code == 500