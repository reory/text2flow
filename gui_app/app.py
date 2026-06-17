"""Main Text2Flow GUI Application"""

import tkinter as tk
from tkinter import filedialog, messagebox
import threading

from gui_app.constants import *
from gui_app.ui import create_main_layout, create_status_bar
from gui_app.handlers.render import render_flowchart_thread, display_svg_preview
from gui_app.handlers.export import export_diagram, get_export_format_config


# ruff: noqa
class Text2FlowGUI:
    """Main GUI Application Class"""

    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=MAIN_BG)

        self.current_svg = None
        self.current_edges = None

        # Initialize UI
        self.status_var = tk.StringVar(value=STATUS_READY)
        self._setup_ui()

    def _setup_ui(self):
        """Setup UI components"""
        # Create main layout
        self.text_input, self.canvas = create_main_layout(
            self.root,
            render_callback=self.render_flowchart,
            clear_callback=self.clear_input,
            export_callback=self.export_diagram,
            on_mousewheel_callback=self.on_mousewheel,
        )

        # Create status bar
        create_status_bar(self.root, self.status_var)

    def render_flowchart(self):
        """Render flowchart (entry point)"""
        text = self.text_input.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning(ERROR_DIALOG_PARSE, ERROR_NO_INPUT)
            return

        # Update status
        self.status_var.set(STATUS_PARSING)
        self.root.update()

        # Run rendering in background thread
        thread = threading.Thread(target=self._render_background, args=(text,))
        thread.daemon = True
        thread.start()

    def _render_background(self, text):
        """Background rendering execution"""

        def on_success(svg_bytes, edges, edge_count):
            """Handle successful rendering"""
            self.current_svg = svg_bytes
            self.current_edges = edges

            # Display preview
            success, message = display_svg_preview(self.canvas, svg_bytes)
            self.status_var.set(STATUS_SUCCESS.format(edge_count))
            self.root.update()

        def on_error(error_type, error_message, status_msg):
            """Handle rendering error"""
            messagebox.showerror(ERROR_DIALOG_RENDER, f"{error_type}: {error_message}")
            self.status_var.set(status_msg)
            self.root.update()

        # Update status
        self.status_var.set(STATUS_RENDERING)
        self.root.update()

        # Perform rendering
        render_flowchart_thread(text, on_success, on_error)

    def export_diagram(self, format_type):
        """Export diagram (entry point)"""
        if self.current_edges is None:
            messagebox.showwarning("No Diagram", ERROR_NO_DIAGRAM)
            return

        # Get file path from user
        default_ext, file_types = get_export_format_config(format_type)
        file_path = filedialog.asksaveasfilename(
            defaultextension=default_ext, filetypes=file_types
        )

        if not file_path:
            return

        # Update status
        self.status_var.set(STATUS_EXPORTING.format(format_type.upper()))
        self.root.update()

        # Perform export
        self._export_background(format_type, file_path)

    def _export_background(self, format_type, file_path):
        """Background export execution"""

        def on_success(message, status):
            """Handle successful export"""
            messagebox.showinfo(ERROR_DIALOG_SUCCESS, message)
            self.status_var.set(status)
            self.root.update()

        def on_error(message):
            """Handle export error"""
            messagebox.showerror(ERROR_DIALOG_EXPORT, message)
            self.status_var.set("Export failed")
            self.root.update()

        # Perform export
        export_diagram(self.current_edges, format_type, file_path, on_success, on_error)

    def on_mousewheel(self, event):
        """Handle mouse wheel zoom"""
        pass  # Implement zoom if needed

    def clear_input(self):
        """Clear input text and canvas"""
        self.text_input.delete("1.0", tk.END)
        self.canvas.delete("all")
        self.current_edges = None
        self.current_svg = None
        self.status_var.set(STATUS_READY)
