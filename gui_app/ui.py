"""UI Layout and Widget Creation"""

import tkinter as tk
from tkinter import scrolledtext

from gui_app.constants import *


# ruff: noqa
def create_header(root):
    """Create header frame with title"""
    header = tk.Frame(root, bg=HEADER_BG, height=50)
    header.pack(fill=tk.X, padx=0, pady=0)
    header.pack_propagate(False)

    title = tk.Label(
        header, text=TITLE_TEXT, font=FONT_TITLE, fg=TEXT_FG_WHITE, bg=HEADER_BG
    )
    title.pack(pady=10)

    return header


def create_left_panel(parent, render_callback, clear_callback):
    """Create left input panel"""
    left_panel = tk.Frame(parent, bg=PANEL_BG, relief=tk.SUNKEN, bd=1)
    left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

    # Input label
    input_label = tk.Label(left_panel, text=INPUT_LABEL, font=FONT_LABEL, bg=PANEL_BG)
    input_label.pack(anchor=tk.W, padx=PADX_INNER, pady=(PADY_INNER, 5))

    # Text input
    text_input = scrolledtext.ScrolledText(
        left_panel, width=40, height=20, font=FONT_INPUT, wrap=tk.WORD
    )
    text_input.pack(fill=tk.BOTH, expand=True, padx=PADX_INNER, pady=(0, 10))
    text_input.insert(tk.END, DEFAULT_INPUT_TEXT)

    # Button frame
    button_frame = tk.Frame(left_panel, bg=PANEL_BG)
    button_frame.pack(fill=tk.X, padx=PADX_INNER, pady=10)

    render_btn = tk.Button(
        button_frame,
        text=BTN_RENDER,
        command=render_callback,
        bg=BTN_RENDER_BG,
        fg=TEXT_FG_WHITE,
        font=FONT_LABEL,
        padx=15,
        pady=8,
    )
    render_btn.pack(side=tk.LEFT, padx=(0, 5))

    clear_btn = tk.Button(
        button_frame,
        text=BTN_CLEAR,
        command=clear_callback,
        bg=BTN_CLEAR_BG,
        fg=TEXT_FG_WHITE,
        font=FONT_LABEL,
        padx=15,
        pady=8,
    )
    clear_btn.pack(side=tk.LEFT, padx=(0, 5))

    return left_panel, text_input


def create_right_panel(parent, export_callback, on_mousewheel_callback):
    """Create right preview and export panel"""
    right_panel = tk.Frame(parent, bg=PANEL_BG, relief=tk.SUNKEN, bd=1)
    right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

    # Preview label
    preview_label = tk.Label(
        right_panel, text=PREVIEW_LABEL, font=FONT_LABEL, bg=PANEL_BG
    )
    preview_label.pack(anchor=tk.W, padx=PADX_INNER, pady=(PADY_INNER, 5))

    # Canvas
    canvas = tk.Canvas(right_panel, bg=PANEL_BG, cursor="hand2", relief=tk.SUNKEN, bd=1)
    canvas.pack(fill=tk.BOTH, expand=True, padx=PADX_INNER, pady=(0, 10))
    canvas.bind("<MouseWheel>", on_mousewheel_callback)
    canvas.bind("<Button-4>", on_mousewheel_callback)
    canvas.bind("<Button-5>", on_mousewheel_callback)

    # Export frame
    export_frame = tk.Frame(right_panel, bg=PANEL_BG)
    export_frame.pack(fill=tk.X, padx=PADX_INNER, pady=10)

    tk.Label(export_frame, text=EXPORT_LABEL, font=FONT_LABEL_SMALL, bg=PANEL_BG).pack(
        side=tk.LEFT, padx=(0, 10)
    )

    svg_btn = tk.Button(
        export_frame,
        text=BTN_EXPORT_SVG,
        command=lambda: export_callback("svg"),
        bg=BTN_EXPORT_BG,
        fg=TEXT_FG_WHITE,
        font=FONT_LABEL_SMALL,
        padx=10,
        pady=5,
    )
    svg_btn.pack(side=tk.LEFT, padx=(0, 5))

    png_btn = tk.Button(
        export_frame,
        text=BTN_EXPORT_PNG,
        command=lambda: export_callback("png"),
        bg=BTN_EXPORT_BG,
        fg=TEXT_FG_WHITE,
        font=FONT_LABEL_SMALL,
        padx=10,
        pady=5,
    )
    png_btn.pack(side=tk.LEFT, padx=(0, 5))

    pdf_btn = tk.Button(
        export_frame,
        text=BTN_EXPORT_PDF,
        command=lambda: export_callback("pdf"),
        bg=BTN_EXPORT_BG,
        fg=TEXT_FG_WHITE,
        font=FONT_LABEL_SMALL,
        padx=10,
        pady=5,
    )
    pdf_btn.pack(side=tk.LEFT)

    return right_panel, canvas


def create_main_layout(
    root, render_callback, clear_callback, export_callback, on_mousewheel_callback
):
    """Create entire main layout"""
    # Header
    create_header(root)

    # Main container
    main_container = tk.Frame(root, bg=MAIN_BG)
    main_container.pack(fill=tk.BOTH, expand=True, padx=PADX_MAIN, pady=PADY_MAIN)

    # Left and right panels
    left_panel, text_input = create_left_panel(
        main_container, render_callback, clear_callback
    )
    right_panel, canvas = create_right_panel(
        main_container, export_callback, on_mousewheel_callback
    )

    return text_input, canvas


def create_status_bar(root, status_var):
    """Create status bar"""
    status_bar = tk.Label(
        root, textvariable=status_var, bg=STATUS_BG, anchor=tk.W, padx=10, pady=5
    )
    status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    return status_bar
