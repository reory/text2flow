"""Unit tests targeting the layout configurations and headless widget creation chains."""

from unittest.mock import MagicMock, patch
import pytest  # noqa
import tkinter as tk
from gui_app import constants as c
from gui_app.ui import (
    create_header,
    create_left_panel,
    create_right_panel,
    create_main_layout,
    create_status_bar,
)


@patch("gui_app.ui.tk.Frame")
@patch("gui_app.ui.tk.Label")
def test_create_header_widget(mock_label, mock_frame):
    """Verify initialization settings, title prompts, and background framing styles."""

    root = MagicMock()
    header = create_header(root)

    # Verify primary structural boundary setup
    mock_frame.assert_called_once_with(root, bg=c.HEADER_BG, height=50)
    mock_frame.return_value.pack.assert_called_once_with(fill=tk.X, padx=0, pady=0)
    mock_frame.return_value.pack_propagate.assert_called_once_with(False)

    # Verify visual text title labels inside the frame header block
    mock_label.assert_called_once_with(
        mock_frame.return_value,
        text=c.TITLE_TEXT,
        font=c.FONT_TITLE,
        fg=c.TEXT_FG_WHITE,
        bg=c.HEADER_BG,
    )
    mock_label.return_value.pack.assert_called_once_with(pady=10)
    assert header == mock_frame.return_value


@patch("gui_app.ui.tk.Frame")
@patch("gui_app.ui.tk.Label")
@patch("gui_app.ui.tk.Button")
@patch("gui_app.ui.scrolledtext.ScrolledText")
def test_create_left_panel_inputs(mock_scrolled, mock_button, mock_label, mock_frame):
    """
    Verify input fields layout rules, scroll configurations,
    and operational action buttons.
    """

    parent = MagicMock()
    render_cb = MagicMock()
    clear_cb = MagicMock()

    left_panel, text_input = create_left_panel(parent, render_cb, clear_cb)

    # Verify core input field setup and text insertion
    mock_scrolled.return_value.insert.assert_called_once_with(
        tk.END, c.DEFAULT_INPUT_TEXT
    )
    assert text_input == mock_scrolled.return_value

    # Verify that action execution buttons were mounted with correct callbacks
    assert mock_button.call_count == 2

    # Validate 'Render' button specifications
    _, render_kwargs = mock_button.call_args_list[0]
    assert render_kwargs["text"] == c.BTN_RENDER
    assert render_kwargs["command"] == render_cb

    # Validate 'Clear' button specifications
    _, clear_kwargs = mock_button.call_args_list[1]
    assert clear_kwargs["text"] == c.BTN_CLEAR
    assert clear_kwargs["command"] == clear_cb


@patch("gui_app.ui.tk.Frame")
@patch("gui_app.ui.tk.Label")
@patch("gui_app.ui.tk.Button")
@patch("gui_app.ui.tk.Canvas")
def test_create_right_panel_preview(mock_canvas, mock_button, mock_label, mock_frame):
    """
    Verify output canvas element generation,
    mousewheel tracking hooks, and export buttons.
    """

    parent = MagicMock()
    export_cb = MagicMock()
    mousewheel_cb = MagicMock()

    right_panel, canvas = create_right_panel(parent, export_cb, mousewheel_cb)

    # Verify canvas interactivity bindings are wired up
    assert mock_canvas.return_value.bind.call_count == 3
    mock_canvas.return_value.bind.assert_any_call("<MouseWheel>", mousewheel_cb)
    assert canvas == mock_canvas.return_value

    # Verify file conversion elements and execute lambda callbacks for full test coverage
    assert mock_button.call_count == 3
    target_formats = ["svg", "png", "pdf"]

    for idx, format_ext in enumerate(target_formats):
        _, btn_kwargs = mock_button.call_args_list[idx]
        lambda_command = btn_kwargs["command"]

        # Invoke closure lambda to score coverage lines
        lambda_command()
        export_cb.assert_called_with(format_ext)


@patch("gui_app.ui.create_header")
@patch("gui_app.ui.create_left_panel")
@patch("gui_app.ui.create_right_panel")
@patch("gui_app.ui.tk.Frame")
def test_create_main_layout_orchestration(
    mock_frame, mock_right, mock_left, mock_header
):
    """Verify that layout sub-components arrange within the main engine framework."""

    root = MagicMock()
    render_cb, clear_cb, export_cb, mw_cb = (
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )

    mock_left.return_value = (MagicMock(), "mock_text_input")
    mock_right.return_value = (MagicMock(), "mock_canvas")

    txt, canv = create_main_layout(root, render_cb, clear_cb, export_cb, mw_cb)

    # Ensure nested elements are initialized
    mock_header.assert_called_once_with(root)
    mock_frame.assert_called_once()
    mock_left.assert_called_once()
    mock_right.assert_called_once()

    assert txt == "mock_text_input"
    assert canv == "mock_canvas"


@patch("gui_app.ui.tk.Label")
def test_create_status_bar(mock_label):
    """Verify application footers establish clean tracking variable links."""

    root = MagicMock()
    status_var = MagicMock()

    status_bar = create_status_bar(root, status_var)

    mock_label.assert_called_once_with(
        root, textvariable=status_var, bg=c.STATUS_BG, anchor=tk.W, padx=10, pady=5
    )
    mock_label.return_value.pack.assert_called_once_with(fill=tk.X, side=tk.BOTTOM)
    assert status_bar == mock_label.return_value
