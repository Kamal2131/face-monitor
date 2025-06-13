from fastapi import APIRouter, Request, Form, Depends, status, File, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import models, auth
from app.database import get_db
from PIL import Image
import os, io, re
import dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Load .env file
dotenv.load_dotenv(dotenv.find_dotenv())

# Cloudinary Config
cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
api_key = os.getenv("CLOUDINARY_API_KEY")
api_secret = os.getenv("CLOUDINARY_API_SECRET")

if not all([cloud_name, api_key, api_secret]):
    raise RuntimeError("Missing Cloudinary credentials in .env")

cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret
)

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
    face_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    MAX_FILE_SIZE = 5 * 1024 * 1024
    ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}

    def sanitize_filename(name: str) -> str:
        return re.sub(r'[^a-zA-Z0-9_]', '', name)

    # Check if username already exists
    if db.query(models.User).filter_by(name=name).first():
        return templates.TemplateResponse("register.html", {"request": request, "msg": "Username already exists"})

    # Validate image size and type
    if face_image.size and face_image.size > MAX_FILE_SIZE:  # type: ignore
        return templates.TemplateResponse("register.html", {"request": request, "msg": "File too large (max 5MB)"})
    if face_image.content_type not in ALLOWED_MIME_TYPES:
        return templates.TemplateResponse("register.html", {"request": request, "msg": "Only JPEG/PNG images allowed"})

    # Read image
    contents = await face_image.read()
    try:
        Image.open(io.BytesIO(contents)).verify()
    except Exception as e:
        return templates.TemplateResponse("register.html", {"request": request, "msg": f"Invalid image file: {str(e)}"})

    safe_name = sanitize_filename(name)
    if not safe_name:
        return templates.TemplateResponse("register.html", {"request": request, "msg": "Invalid username format"})

    # Upload to Cloudinary
    try:
        upload_result = cloudinary.uploader.upload(
            io.BytesIO(contents),
            public_id=f"faces/{safe_name}",
            overwrite=True,
            resource_type="image"
        )
        image_url = upload_result["secure_url"]
    except Exception as e:
        return templates.TemplateResponse("register.html", {"request": request, "msg": f"Upload failed: {str(e)}"})

    # Create new user
    try:
        hashed = auth.hash_password(password)
        new_user = models.User(
            name=safe_name,
            password_hash=hashed,
            role=role,
            image_url=image_url  # Add this field to your model if not already present
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
    if not user or not auth.verify_password(password, user.password_hash):  # type: ignore
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid credentials"})

    redirect_url = "/admin/dashboard" if user.role == "admin" else "/dashboard" # type: ignore
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user", value=name, httponly=True, samesite="Lax") # type: ignore
    return response


@router.get("/api/current-user")
async def get_current_user_endpoint(user: str = Depends(auth.get_current_username)):
    return {"name": user}
