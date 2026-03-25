# FastAPI entry point.
# Loads routers, templates, static files.

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import ui, api

app = FastAPI(title="Text2Flow")

# Create one templates instance
templates = Jinja2Templates(directory="app/templates")

# Attach it to apps.state before including routers
app.state.templates = templates

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routers
app.include_router(ui.router)
app.include_router(api.router)