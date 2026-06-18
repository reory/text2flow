from unittest.mock import MagicMock, mock_open, patch
import pytest  # noqa
from gui_app import constants as c
from gui_app.handlers.export import export_diagram, get_export_format_config

"""
Testing file-system interactions.
Python's built-in mock_open, which acts as a fake file system in memory.
"""


@patch("gui_app.handlers.export.render_flowchart")
def test_export_diagram_success(mock_render):
    """
    Verify that a successful file export writes binary data and triggers
    success closures.
    """

    mock_render.return_value = b"mock_binary_image_data"
    on_success = MagicMock()
    on_error = MagicMock()
    fake_file_system = mock_open()

    # Intercept built-in open() calls to avoid altering the developer's hard drive
    with patch("builtins.open", fake_file_system):
        export_diagram(
            edges=[("A", "B")],
            format_type="png",
            file_path="C:/workspace/my_chart.png",
            on_success=on_success,
            on_error=on_error,
        )

    # Verify rendering engine was invoked properly
    mock_render.assert_called_once_with([("A", "B")], format="png")

    # Verify file stream actions occurred precisely as intended
    fake_file_system.assert_called_once_with("C:/workspace/my_chart.png", "wb")
    fake_file_system().write.assert_called_once_with(b"mock_binary_image_data")

    # Confirm correct messages routed back to the UI controller layer
    expected_success_msg = "Diagram exported to:\nC:/workspace/my_chart.png"
    expected_status_msg = c.STATUS_EXPORTED.format("PNG")
    on_success.assert_called_once_with(expected_success_msg, expected_status_msg)
    on_error.assert_not_called()


@patch("gui_app.handlers.export.render_flowchart")
def test_export_diagram_io_exception_catch(mock_render):
    """Verify disk write errors or render crashes are safely caught."""

    mock_render.return_value = b"some_bytes"
    on_success = MagicMock()
    on_error = MagicMock()

    fake_file_system = mock_open()
    # Simulate a file writing crash (e.g., OS permission denied error)
    fake_file_system().write.side_effect = IOError(
        "Permission denied writing to protected folder"
    )

    with patch("builtins.open", fake_file_system):
        export_diagram([("A", "B")], "pdf", "restricted.pdf", on_success, on_error)

    on_success.assert_not_called()
    on_error.assert_called_once_with(
        "Failed to export:\nPermission denied writing to protected folder"
    )


def test_get_export_format_config_valid_match():
    """
    Verify configuration tuple lookups map out extensions matching
    configuration constants.
    """
    default_ext, file_types = get_export_format_config("png")

    assert default_ext == ".png"
    assert file_types == [("PNG files", "*.png"), ("All files", "*.*")]


def test_get_export_format_config_unsupported_type():
    """
    Verify fallback response structure if an invalid or unsupported file
    type is requested.
    """

    default_ext, file_types = get_export_format_config("unknown_format_ext")

    assert default_ext is None
    assert file_types == []
