# Handles the browser-facing routes:
# Editor page
# Preview → returns rendered PNG for preview

from fastapi import APIRouter, Request

router = APIRouter()

def get_templates(request: Request):

    return request.app.state.templates

@router.get("/")
def editor(request: Request):

    templates = request.app.state.templates
    
    return templates.TemplateResponse(
        request=request,
        name="editor.html", 
        context={}
    )