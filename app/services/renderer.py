# Graphviz rendering engine.

from graphviz import Digraph

def render_flowchart(edges, format: str = "png"):
    """
    Render flowchart to specified format (png, svg, pdf, etc.)
    
    Args:
        edges: List of (source, destination) tuples
        format: Output format ('png', 'svg', 'pdf', etc.)
    
    Returns:
        Rendered diagram bytes
    """
    dot = Digraph(format=format)
    dot.attr(rankdir="TB")  # TB Top to Bottom layout
    
    for src, dst in edges:
        dot.edge(src, dst)

    return dot.pipe()