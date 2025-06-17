# app/routes/dashboard_routes.py
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import status
from app.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
async def dashboard(request: Request, user=Depends(get_current_user)):
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user
    })

@router.get("/recognize")
async def recognize(request: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("recognize.html", {"request": request, "user": user})


@router.get("/about")
def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
