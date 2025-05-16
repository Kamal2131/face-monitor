# app/main.py
from fastapi import FastAPI, Request, Form, Depends, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app import database, models, auth
import shutil
import os

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return RedirectResponse("/login")

@app.get("/register")
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_post(
    request: Request,
    name: str = Form(...),
    password: str = Form(...),
    face_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(models.User.name == name).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": request, "msg": "User already exists!"})

    # Save image
    filename = f"{name}.jpg"
    image_path = f"app/static/uploads/{filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(face_image.file, buffer)

    # Save user with password
    hashed = auth.hash_password(password)
    user = models.User(name=name, password_hash=hashed)
    db.add(user)
    db.commit()

    return RedirectResponse("/login", status_code=303)


@app.get("/login")
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login_post(request: Request, name: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == name).first()
    if not user or not auth.verify_password(password, user.password_hash):
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid credentials"})
    return RedirectResponse("/dashboard", status_code=303)

# Home or dashboard
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("recognize.html", {"request": request})


# Warning endpoint
@app.post("/raise-warning")
async def raise_warning(request: Request):
    data = await request.json()
    reason = data.get("reason")
    timestamp = data.get("timestamp")

    print(f"⚠️ Suspicious Activity: {reason} at {timestamp}")

    # Save to file (optional)
    with open("warnings.log", "a") as f:
        f.write(f"{timestamp} - {reason}\n")

    return JSONResponse(content={"message": "Warning received"}, status_code=200)

@app.get("/recognize", response_class=HTMLResponse)
async def recognize_page(request: Request):
    return templates.TemplateResponse("recognize.html", {"request": request})
