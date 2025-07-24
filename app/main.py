from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import auth_routes, dashboard_routes, proctor_routes, admin, quiz, quiz_scores, leaderboard
from app.database import Base, engine
from app.middleware import auth_middleware
from fastapi.responses import RedirectResponse

# Initialize DB tables
Base.metadata.create_all(bind=engine)
app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Add static URL to all templates
templates.env.globals["static_url"] = "/static"

# Add middleware
app.middleware("http")(auth_middleware)

# Include routers
app.include_router(auth_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(proctor_routes.router)
app.include_router(admin.router)
app.include_router(quiz.router)
app.include_router(quiz_scores.router)
app.include_router(leaderboard.router)



@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return templates.TemplateResponse("login_required.html", {"request": request}, status_code=401)
    elif exc.status_code == 403:
        return templates.TemplateResponse("not_authorized.html", {"request": request}, status_code=403)
    return await http_exception_handler(request, exc)