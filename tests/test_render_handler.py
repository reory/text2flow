"""Unit tests targeting the UI background threading and canvas render handler handlers."""

import tkinter as tk
from unittest.mock import MagicMock, patch

import pytest  # noqa

from gui_app import constants as c
from gui_app.handlers.render import display_img_preview, render_flowchart_thread


@patch("gui_app.handlers.render.parse_edges")
@patch("gui_app.handlers.render.render_flowchart")
def test_render_flowchart_thread_success(mock_render, mock_parse):
    """
    Verify clean text rendering execution fires the success hook with
    structured data.
    """

    on_success = MagicMock()
    on_error = MagicMock()

    mock_parse.return_value = [("A", "B"), ("B", "C")]
    mock_render.return_value = b"<svg>mock_output</svg>"

    render_flowchart_thread("A -> B -> C", "dot", on_success, on_error)

    # Confirm core services were executed correctly
    mock_parse.assert_called_once_with("A -> B -> C")
    mock_render.assert_called_once_with(
        [("A", "B"), ("B", "C")], 
        format="png",
        engine="dot",
    )

    # Confirm the success closure callback fired with expected counts
    on_success.assert_called_once_with(
        b"<svg>mock_output</svg>", [("A", "B"), ("B", "C")], 2
    )
    on_error.assert_not_called()


@patch("gui_app.handlers.render.parse_edges")
def test_render_flowchart_thread_validation_failure(mock_parse):
    """Verify syntax ValueErrors are safely intercepted and dispatched to on_error."""

    on_success = MagicMock()
    on_error = MagicMock()

    mock_parse.side_effect = ValueError("Syntax error: dangling relationship link")

    render_flowchart_thread("A ->", "dot", on_success, on_error)

    on_success.assert_not_called()
    on_error.assert_called_once_with(
        "ValueError", "Syntax error: dangling relationship link", c.STATUS_ERROR_PARSE
    )


@patch("gui_app.handlers.render.parse_edges")
def test_render_flowchart_thread_generic_system_crash(mock_parse):
    """
    Verify runtime Exceptions are caught safely to avoid
    crashing background workers.
    """

    on_success = MagicMock()
    on_error = MagicMock()

    mock_parse.side_effect = Exception("System environment out of memory breakdown")

    render_flowchart_thread("A -> B", "dot", on_success, on_error)

    on_success.assert_not_called()
    on_error.assert_called_once_with(
        "Exception", "System environment out of memory breakdown", c.STATUS_ERROR_RENDER
    )

@patch("gui_app.handlers.render.tk.PhotoImage")
def test_display_img_preview_success(mock_photo):
    """
    Verify vector raw bytes parse into textual
    notifications inside the window grid.
    """

    mock_image = MagicMock()
    mock_photo.return_value = mock_image

    canvas = MagicMock()
    # Stub out dimensions so floor division computations don't throw TypeErrors
    canvas.winfo_width.return_value = 800
    canvas.winfo_height.return_value = 600

    success, message = display_img_preview(
        canvas, b"fake_png_binary_bytes"
    )

    assert success is True
    assert message == c.STATUS_SVG_READY

    # Ensure canvas actions scrubbed previous prints and rendered image in the center
    canvas.delete.assert_called_once_with("all")
    canvas.create_image.assert_called_once_with(
        400,
        300,
        image=mock_image,
        anchor=tk.CENTER,
    )

    assert canvas.image is mock_image


def test_display_img_preview_exception_catch():
    """
    Verify canvas failures return an error notification tuple
    gracefully instead of blowing up.
    """

    canvas = MagicMock()
    # Force a canvas operational crash when clearing elements
    canvas.delete.side_effect = RuntimeError(
        "Tkinter context destroyed or dead thread context"
    )

    success, message = display_img_preview(canvas, b"<svg>data</svg>")

    assert success is False
    assert "Display error: Tkinter context destroyed" in message
