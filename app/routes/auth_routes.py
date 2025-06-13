# app/routes/auth_routes.py
from fastapi import APIRouter, Request, Form, Depends, status, File, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import models, auth
from app.database import get_db
from PIL import Image
import os, io, re

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
    role: str = Form("student"),  # default role is student
    face_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    MAX_FILE_SIZE = 5 * 1024 * 1024
    ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}

    def sanitize_filename(name: str) -> str:
        return re.sub(r'[^a-zA-Z0-9_]', '', name)

    if db.query(models.User).filter_by(name=name).first():
        return templates.TemplateResponse("register.html", {"request": request, "msg": "Username already exists"})

    if face_image.size > MAX_FILE_SIZE:  # type: ignore
        return templates.TemplateResponse("register.html", {"request": request, "msg": "File too large (max 5MB)"})

    if face_image.content_type not in ALLOWED_MIME_TYPES:
        return templates.TemplateResponse("register.html", {"request": request, "msg": "Only JPEG/PNG images allowed"})

    contents = await face_image.read()
    try:
        Image.open(io.BytesIO(contents)).verify()
    except Exception as e:
        return templates.TemplateResponse("register.html", {"request": request, "msg": f"Invalid image file: {str(e)}"})

    safe_name = sanitize_filename(name)
    if not safe_name:
        return templates.TemplateResponse("register.html", {"request": request, "msg": "Invalid username format"})

    upload_dir = "app/static/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{safe_name}.jpg")

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
    except IOError as e:
        return templates.TemplateResponse("register.html", {"request": request, "msg": f"File save failed: {str(e)}"})

    try:
        hashed = auth.hash_password(password)
        new_user = models.User(name=safe_name, password_hash=hashed, role=role)
        db.add(new_user)
        db.commit()
    except Exception as e:
        db.rollback()
        if os.path.exists(file_path):
            os.remove(file_path)
        return templates.TemplateResponse("register.html", {"request": request, "msg": f"Registration failed: {str(e)}"})

    # Redirect based on role
    redirect_url = "/admin/dashboard" if role == "admin" else "/dashboard"
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user", value=safe_name, httponly=True, samesite="Lax", max_age=3600)  # type: ignore
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
    if not user or not auth.verify_password(password, user.password_hash):  # type: ignore
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid credentials"})

    redirect_url = "/admin/dashboard" if user.role == "admin" else "/dashboard" # type: ignore
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user", value=name, httponly=True, samesite="Lax")  # type: ignore
    return response

@router.get("/api/current-user")
async def get_current_user_endpoint(user: str = Depends(auth.get_current_username)):
    return {"name": user}

