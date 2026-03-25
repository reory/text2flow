# services/parser.py
# Your text → edges logic lives here.

def parse_edges(text: str):
    edges = []
    # Split into lines and remove completely empty ones
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    for line in lines:
        if "->" not in line:
            # This is likely what is triggering your 400 error
            raise ValueError(f"Invalid syntax: {line}")
        
        parts = [part.strip() for part in line.split("->")]
        
        # Handle cases like "A -> B -> C"
        for i in range(len(parts) - 1):
            src = parts[i]
            dst = parts[i+1]
            if src and dst:
                edges.append((src, dst))
                
    return edges