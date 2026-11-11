"""Export Handler"""

from app.services.renderer import render_flowchart
from gui_app.constants import *


# ruff: noqa
def export_diagram(edges, format_type, file_path, on_success, on_error):
    """Export diagram to file."""

    try:
        # Render to specified format
        image_bytes = render_flowchart(edges, format=format_type)

        # Write to file
        with open(file_path, "wb") as f:
            f.write(image_bytes)

        success_msg = f"Diagram exported to:\n{file_path}"
        status_msg = STATUS_EXPORTED.format(format_type.upper())
        on_success(success_msg, status_msg)

    except Exception as e:
        error_msg = f"Failed to export:\n{str(e)}"
        on_error(error_msg)


def get_export_format_config(format_type):
    """Get file dialog configuration for export format."""

    config = EXPORT_FORMATS.get(format_type)
    if config:
        return f".{format_type}", [config, ("All files", "*.*")]
    return None, []
