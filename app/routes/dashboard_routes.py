# app/routes/dashboard_routes.py
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import status
from app.auth import get_current_user
from app.services.dashboard import get_dashboard_data
from app.database import get_db, Session
from app.models import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", name="home_page")
async def home(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("home.html", {"request": request, "user": user})


@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    context = get_dashboard_data(db, current_user)
    context["request"] = request
    return templates.TemplateResponse("dashboard.html", context)

@router.get("/recognize")
async def recognize(request: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("recognize.html", {"request": request, "user": user})


@router.get("/about")
def about_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("about.html", {"request": request, "user": user})
