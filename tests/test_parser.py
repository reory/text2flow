import pytest
from hypothesis import given, strategies as st
from app.services.parser import parse_edges, ParsedDiagram


def test_parse_basic_edges():
    """Verify standard flowchart connections parse correctly"""

    text = "A -> B\nB -> C"
    result = parse_edges(text)

    assert isinstance(result, ParsedDiagram)
    assert list(result) == [("A", "B"), ("B", "C")]


def test_parse_node_attributes():
    """Verify styling attributes are extracted properly"""

    text = "Alpha [fillcolor=lightblue, shape=box]"
    result = parse_edges(text)

    assert "Alpha" in result.nodes
    assert result.nodes["Alpha"]["fillcolor"] == "lightblue"
    assert result.nodes["Alpha"]["shape"] == "box"


def test_parser_syntax_error():
    """Verify bad text inputs trigger an explicit ValueError"""

    with pytest.raises(ValueError, match="Invalid syntax"):
        parse_edges("This is completely invalid syntax lines")


@given(st.text())
def test_parser_never_crashes_with_random_input(random_string):
    """
    Hypothesis Property Test: No matter what garbage text is typed,
    the parser must either successfully process it or throw an expected ValueError.
    It should NEVER throw an unhandled IndexError or crash entirely
    """

    try:
        parse_edges(random_string)
    except ValueError:
        pass
