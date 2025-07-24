from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import models, auth
from app.database import get_db
import re

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/register")
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register_post(
    request: Request,
    name: str = Form(...),
    password: str = Form(...),
    role: str = Form("student"),
    db: Session = Depends(get_db)
):
    def sanitize_filename(name: str) -> str:
        return re.sub(r'[^a-zA-Z0-9_]', '', name)

    if db.query(models.User).filter_by(name=name).first():
        return templates.TemplateResponse("register.html", {"request": request, "msg": "Username already exists"})

    safe_name = sanitize_filename(name)
    if not safe_name:
        return templates.TemplateResponse("register.html", {"request": request, "msg": "Invalid username format"})

    try:
        hashed = auth.hash_password(password)
        new_user = models.User(
            name=safe_name,
            password_hash=hashed,
            role=role
        )
        db.add(new_user)
        db.commit()
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse("register.html", {"request": request, "msg": f"Registration failed: {str(e)}"})

    redirect_url = "/admin/dashboard" if role == "admin" else "/dashboard"
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user", value=safe_name, httponly=True, samesite="Lax", max_age=3600) # type: ignore
    return response

@router.get("/login")
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_post(
    request: Request,
    name: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter_by(name=name).first()
    if not user or not auth.verify_password(password, user.password_hash): # type: ignore
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid credentials"})

    redirect_url = "/admin/dashboard" if user.role == "admin" else "/dashboard" # type: ignore
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user", value=name, httponly=True, samesite="Lax") # type: ignore
    return response

@router.get("/logout-confirm")
def logout_confirm(request: Request):
    return templates.TemplateResponse("logout_confirm.html", {"request": request})

@router.get("/logout")
def logout(request: Request):
    response = templates.TemplateResponse("logout.html", {"request": request})
    response.delete_cookie("user")
    return response

@router.get("/api/current-user")
async def get_current_user_endpoint(user: str = Depends(auth.get_current_username), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(name=user).first()
    if not db_user:
        return {"error": "User not found"}
    return {
        "name": db_user.name
        # "image_url": db_user.image_url  # Uncomment only if it's defined in model
    }
