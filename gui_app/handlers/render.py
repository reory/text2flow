"""Rendering Handler"""

from app.services.parser import parse_edges
from app.services.renderer import render_flowchart
from gui_app.constants import *


# ruff: noqa
def render_flowchart_thread(text, on_success, on_error):
    """Background rendering thread handler

    Args:
        text: Input text to parse
        on_success: Callback function(svg_bytes) on success
        on_error: Callback function(error_type, error_message) on error
    """
    try:
        # Parse edges
        edges = parse_edges(text)

        # Render as SVG
        image_bytes = render_flowchart(edges, format="svg")

        # Call success callback
        on_success(image_bytes, edges, len(edges))

    except ValueError as e:
        on_error("ValueError", str(e), STATUS_ERROR_PARSE)
    except Exception as e:
        on_error("Exception", str(e), STATUS_ERROR_RENDER)


def display_svg_preview(canvas, svg_bytes):
    """Display SVG preview in canvas

    Args:
        canvas: Tkinter canvas widget
        svg_bytes: SVG content as bytes

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        svg_text = svg_bytes.decode("utf-8")

        # Clear canvas
        canvas.delete("all")

        # Create info text
        info_text = f"SVG Flowchart\n({len(svg_text)} bytes)"
        canvas.create_text(
            canvas.winfo_width() // 2,
            canvas.winfo_height() // 2,
            text=info_text,
            font=("Arial", 14),
            fill=TEXT_FG,
        )

        return True, STATUS_SVG_READY

    except Exception as e:
        return False, f"Display error: {str(e)}"
