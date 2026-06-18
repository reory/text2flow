"""Unit tests targeting the GUI constants and style configurations."""
# Validating that the layout numbers and dictionary mappings
# don't accidentally get altered down the road.

import gui_app.constants as c


def test_visual_theme_constants():
    """Verify that user interface theme assets and color hexes are bound properly."""

    assert c.HEADER_BG == "#2c3e50"
    assert c.MAIN_BG == "#f0f0f0"
    assert c.BTN_RENDER_BG == "#27ae60"
    assert c.BTN_CLEAR_BG == "#e74c3c"


def test_window_and_layout_dimensions():
    """Verify default window bounds and padding measurements."""

    assert c.WINDOW_WIDTH == 1200
    assert c.WINDOW_HEIGHT == 700
    assert c.WINDOW_TITLE == "Text2Flow - Flowchart Generator"
    assert c.PADX_MAIN == 10
    assert c.PADY_INNER == 5


def test_text_and_status_strings():
    """Verify critical interface messaging prompts and status formatting hooks."""

    assert "A -> B -> C" in c.INPUT_LABEL
    assert c.STATUS_READY == "Ready"
    assert c.STATUS_SUCCESS == "✓ Successfully rendered {} edges"
    assert c.ERROR_NO_INPUT == "Please enter some text"


def test_export_file_extensions_dictionary():
    """Verify the file types mapping table contains valid dictionary extensions."""

    assert isinstance(c.EXPORT_FORMATS, dict)
    assert "png" in c.EXPORT_FORMATS
    assert "svg" in c.EXPORT_FORMATS
    assert "pdf" in c.EXPORT_FORMATS

    # Confirm structural tuple types match expectations
    label, wildcard = c.EXPORT_FORMATS["png"]
    assert label == "PNG files"
    assert wildcard == "*.png"
