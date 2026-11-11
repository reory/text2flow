"""UI Constants and Configuration"""

# Metallic & Gunmetal Colors
HEADER_BG = "#334155"        # Dark metallic slate
MAIN_BG = "#cbd5e1"          # Brushed silver background
PANEL_BG = "#f8fafc"         # Clean light chrome panel
TEXT_FG = "#1e293b"          # Deep charcoal text
TEXT_FG_WHITE = "white"
BTN_RENDER_BG = "#475569"    # Steel gray render button
BTN_CLEAR_BG = "#64748b"     # Muted gray-blue clear button
BTN_EXPORT_BG = "#94a3b8"    # Metallic silver export button
STATUS_BG = "#e2e8f0"        # Light metallic bar

# Fonts
FONT_TITLE = ("Arial", 16, "bold")
FONT_LABEL = ("Arial", 10, "bold")
FONT_LABEL_SMALL = ("Arial", 9)
FONT_INPUT = ("Courier", 10)
FONT_CANVAS = ("Arial", 14)

# Window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Text2Flow - Flowchart Generator"

# Text Strings
TITLE_TEXT = "Text2Flow - Convert Text to Flowcharts"
INPUT_LABEL = "Input Text (use A -> B -> C format):"
PREVIEW_LABEL = "Preview:"
EXPORT_LABEL = "Export as:"
DEFAULT_INPUT_TEXT = "Start -> Process -> Decision\nDecision -> Success\nDecision -> Failure"

# Button Labels
BTN_RENDER = "Render"
BTN_CLEAR = "Clear"
BTN_EXPORT_SVG = "Export SVG"
BTN_EXPORT_PNG = "Export PNG"
BTN_EXPORT_PDF = "Export PDF"

# Status Messages
STATUS_READY = "Ready"
STATUS_PARSING = "Parsing..."
STATUS_RENDERING = "Rendering..."
STATUS_EXPORTING = "Exporting as {}"
STATUS_SUCCESS = "✓ Successfully rendered {} edges"
STATUS_SVG_READY = "✓ Rendered as SVG (ready to export)"
STATUS_EXPORTED = "✓ Exported as {}"
STATUS_ERROR_PARSE = "Error: Parsing failed"
STATUS_ERROR_RENDER = "Error: Rendering failed"

# Error Messages
ERROR_NO_INPUT = "Please enter some text"
ERROR_NO_DIAGRAM = "Please render a diagram first"
ERROR_DIALOG_PARSE = "Parsing Error"
ERROR_DIALOG_RENDER = "Rendering Error"
ERROR_DIALOG_EXPORT = "Export Error"
ERROR_DIALOG_SUCCESS = "Success"

# File Export Options
EXPORT_FORMATS = {
    "svg": ("SVG files", "*.svg"),
    "png": ("PNG files", "*.png"),
    "pdf": ("PDF files", "*.pdf"),
}

# Layout Padding
PADX_MAIN = 10
PADY_MAIN = 10
PADX_INNER = 10
PADY_INNER = 5
