# Handles programmatic endpoints:
# /api/render → returns PNG/SVG.
# Logger tracks incoming requests and errors.

from fastapi import APIRouter, Response
from pydantic import BaseModel
from app.services.parser import parse_edges
from app.services.renderer import render_flowchart
from app.services.logger import logger

router = APIRouter(prefix="/api")


# 1. Define a schema for the incoming JSON body
class RenderRequest(BaseModel):
    text: str
    format: str = "png"


@router.post("/render")
def render_diagram(payload: RenderRequest):
    """Render diagram from text input."""

    # Extract data from our Pydantic payload
    text = payload.text
    format = payload.format

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
