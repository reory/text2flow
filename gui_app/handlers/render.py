"""Rendering Handler"""

import tkinter as tk

from app.services.parser import parse_edges
from app.services.renderer import render_flowchart
from gui_app.constants import *


def render_flowchart_thread(text, engine, on_success, on_error):
    """Background rendering thread handler."""

    try:
        # Parse edges
        edges = parse_edges(text)

        # Render as PNG
        image_bytes = render_flowchart(edges, format="png", engine=engine)

        # Call success callback
        on_success(image_bytes, edges, len(edges))

    except ValueError as e:
        on_error("ValueError", str(e), STATUS_ERROR_PARSE)
    except (RuntimeError, OSError) as e:
        on_error("SystemError", str(e), STATUS_ERROR_RENDER)
    except Exception as e: # noqa: BLE001
        on_error("Exception", str(e), STATUS_ERROR_RENDER)


def display_img_preview(canvas, image_bytes):
    """Display PNG preview on canvas."""

    try:

        # Clear canvas
        canvas.delete("all")

        img = tk.PhotoImage(data=image_bytes)

        canvas.image = img

        # Create info text
        canvas.create_image(
            canvas.winfo_width() // 2,
            canvas.winfo_height() // 2,
            image=img,
            anchor=tk.CENTER,
        )

        return True, STATUS_SVG_READY

    except Exception as e: # noqa: BLE001
        return False, f"Display error: {e!s}"
