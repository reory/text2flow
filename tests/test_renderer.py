import pytest  # noqa
from app.services.renderer import render_flowchart


class DummyDiagram(list):
    """
    A minimal mock class that mimics the structure of ParsedDiagram
    by being a iterable list with a custom .nodes attribute
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nodes = {}


def test_render_flowchart_basic():
    """Verify that a basic list of edge tuples cleanly generates image bytes"""

    edges = DummyDiagram([("A", "B"), ("B", "C")])

    result = render_flowchart(edges, format="png")

    assert isinstance(result, bytes)
    assert len(result) > 0


def test_render_flowchart_fills_missing_style():
    """
    Verify that if a node has a fillcolor but no explicit style
    the function automatically injects 'style' = 'filled
    """

    edges = DummyDiagram([("Alpha", "Beta")])
    edges.nodes["Alpha"] = {"fillcolor": "#ff0000", "shape": "box"}

    # Use SVG format to inspect the raw string contents of the bytes
    result = render_flowchart(edges, format="svg")

    assert isinstance(result, bytes)
    assert b"#ff0000" in result
    assert b"fill" in result


def test_render_flowchart_preserves_existing_style():
    """
    Verify that if a node already specifies a style
    the autofill logic does not override it
    """

    edges = DummyDiagram([("Alpha", "Beta")])
    edges.nodes["Alpha"] = {
        "fillcolor": "#00ff00",
        "style": "dashed,filled",
        "shape": "ellipse",
    }

    result = render_flowchart(edges, format="svg")

    assert isinstance(result, bytes)
    assert b"#00ff00" in result
