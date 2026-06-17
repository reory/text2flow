# Graphviz rendering engine.

from graphviz import Digraph


def render_flowchart(edges, format: str = "png"):
    """
    Render flowchart to specified format (png, svg, pdf, etc.)
    """
    dot = Digraph(format=format)
    dot.attr(rankdir="TB")  # TB Top to Bottom layout

    nodes_metadata = getattr(edges, "nodes", {})

    # Apply custom node styles first
    for node_name, attrs in nodes_metadata.items():
        if "fillcolor" in attrs and "style" not in attrs:
            attrs["style"] = "filled"

        dot.node(node_name, **attrs)

    # Render connection lines
    for src, dst in edges:
        dot.edge(src, dst)

    return dot.pipe()
