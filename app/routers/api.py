# Handles programmatic endpoints:
# /api/render → returns PNG/SVG.
# Logger tracks incoming requests and errors.

from fastapi import APIRouter, Body, Response
from app.services.parser import parse_edges
from app.services.renderer import render_flowchart
from app.services.logger import logger

router = APIRouter(prefix="/api")

@router.post("/render")
def render_diagram(text: str = Body(..., embed=True), format: str = "png"):
    """
    Render diagram from text input.
    
    Args:
        text: Text with edges in format "A -> B -> C"
        format: Output format ('png', 'svg', 'pdf', etc.)
    """
    # Log first 50 characters
    logger.info(f"Render requested for input: {text[:50]} (format: {format})")

    try:
        edges = parse_edges(text)
        image_bytes = render_flowchart(edges, format=format)
        logger.info(f"Successfully rendered {len(edges)} edges as {format}.")
        
        # Set appropriate media type based on format
        media_types = {
            "png": "image/png",
            "svg": "image/svg+xml",
            "pdf": "application/pdf",
        }
        media_type = media_types.get(format, "application/octet-stream")
        
        return Response(content=image_bytes, media_type=media_type)
    
    except ValueError as ve:
        # Log a warning
        logger.warning(f"Validation failed {ve}")
        return Response(content=str(ve), status_code=400)
    
    except Exception as e:
        # Log an error
        logger.error(f"System error during rendering: {e}", exc_info=True)
        # Return a 500 error
        return Response(content="Internal Server Error", status_code=500)