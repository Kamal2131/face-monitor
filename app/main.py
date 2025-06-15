from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import auth_routes, dashboard_routes, proctor_routes, admin
from app.database import Base, engine
from app.middleware import auth_middleware
from fastapi.responses import RedirectResponse

# Initialize DB tables
Base.metadata.create_all(bind=engine)
app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Add middleware
app.middleware("http")(auth_middleware)

# Include routers
app.include_router(auth_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(proctor_routes.router)
app.include_router(admin.router)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/login")

@app.get("/logout")
def logout(request: Request):
    response = templates.TemplateResponse("logout.html", {"request": request})
    response.delete_cookie("user")
    return response

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
