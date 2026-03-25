# Graphviz rendering engine.

from graphviz import Digraph

def render_flowchart(edges):

    dot = Digraph(format="png")
    dot.attr(rankdir="TB") #TB Top to Bottom layout

    for src, dst in edges:
        dot.edge(src, dst)

    return dot.pipe()