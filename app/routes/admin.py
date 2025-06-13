from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Question
from app.auth import get_current_user

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="app/templates")

# Middleware-like function to check if the user is admin
def require_admin(user: User):
    if (user.role != "admin"): # type: ignore
        raise HTTPException(status_code=403, detail="Admins only")


@router.get("/dashboard")
def admin_dashboard(request: Request, user: User = Depends(get_current_user)):
    require_admin(user)
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "user": user.name})


@router.get("/questions/add")
def add_question_get(request: Request, user: User = Depends(get_current_user)):
    require_admin(user)
    return templates.TemplateResponse("add_question.html", {"request": request})


@router.post("/questions/add")
def add_question_post(
    request: Request,
    question_text: str = Form(...),
    option1: str = Form(...),
    option2: str = Form(...),
    option3: str = Form(...),
    option4: str = Form(...),
    correct_option: int = Form(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    require_admin(user)

    question = Question(
        question_text=question_text,
        option1=option1,
        option2=option2,
        option3=option3,
        option4=option4,
        correct_option=correct_option
    )
    db.add(question)
    db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=303)


@router.get("/users")
def manage_users(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_admin(user)
    users = db.query(User).all()
    return templates.TemplateResponse("manage_users.html", {"request": request, "users": users})


@router.post("/users/promote/{user_id}")
def promote_user(user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_admin(user)
    target_user = db.query(User).filter(User.id == user_id).first()
    if target_user:
        setattr(target_user, "role", "admin")
        db.commit()
    return RedirectResponse("/admin/users", status_code=303)


@router.post("/users/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_admin(user)
    target_user = db.query(User).filter(User.id == user_id).first()
    if target_user:
        db.delete(target_user)
        db.commit()
    return RedirectResponse("/admin/users", status_code=303)
