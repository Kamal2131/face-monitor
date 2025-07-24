from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.auth import get_current_user

from app.database import get_db
from app.models import User, StudentScore

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/leaderboard")
def leaderboard(request: Request, db: Session = Depends(get_db), user1=Depends(get_current_user)):
    # SQLAlchemy expression to calculate percentage
    percentage_expr = (func.sum(StudentScore.score) / func.sum(StudentScore.total) * 100.0).label("percentage")

    leaderboard_data = (
        db.query(
            User.name,
            User.student_id,
            User.course,
            func.sum(StudentScore.score).label("total_score"),
            func.sum(StudentScore.total).label("total_marks"),
            percentage_expr
        )
        .join(StudentScore, StudentScore.user_id == User.id)
        .group_by(User.id)
        .having(func.sum(StudentScore.score) > 10)
        .order_by(percentage_expr.desc())  # ✅ Correct use of desc()
        .all()
    )

    return templates.TemplateResponse("leaderboard.html", {
        "request": request,
        "leaderboard": leaderboard_data, 
        "user": user1,
        
    })
