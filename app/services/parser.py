# services/parser.py
# Your text → edges logic lives here.


class ParsedDiagram(list):
    """
    A backward-compatible list subclass that holds edge tuples
    while attaching custom node metadata on the side
    """

    def __init__(self, edges, nodes=None):
        super().__init__(edges)
        self.nodes = nodes or {}


def parse_edges(text: str):

    nodes = {}
    edges = []

    # Split into lines and remove completely empty ones
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines:
        if "->" in line:
            parts = [part.strip() for part in line.split("->")]

            # Handle cases like "A -> B -> C"
            for i in range(len(parts) - 1):
                src = parts[i]
                dst = parts[i + 1]
                if src and dst:
                    edges.append((src, dst))

        elif "[" in line and line.endswith("]"):
            node_part, attr_part = line.split("[", 1)
            node_name = node_part.strip()
            attrs_str = attr_part.rstrip("]").strip()

            attrs = {}
            # Split individual attributes by commas
            for item in attrs_str.split(","):
                if "=" in item:
                    k, v = item.split("=", 1)
                    # Strip outer whitespace and any single or double quotes around the value
                    attrs[k.strip()] = v.strip().strip('"').strip("'")

            if node_name:
                nodes[node_name] = attrs
        else:
            raise ValueError(
                f"Invalid syntax: '{line}'. Lines must be define an edge (A -> B) "
                f"or atrribute definitions (A [shape=box, color=blue])."
            )

    return ParsedDiagram(edges, nodes=nodes)
