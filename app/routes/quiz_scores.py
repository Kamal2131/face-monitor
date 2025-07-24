from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import StudentScore, User
from app.auth import get_current_user

router = APIRouter()

@router.post("/submit-score")
def submit_score(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    topic = data.get("topic")
    score = data.get("score")
    total = data.get("total")

    if not all([topic, isinstance(score, int), isinstance(total, int)]):
        raise HTTPException(status_code=400, detail="Invalid score data")

    db_score = StudentScore(
        user_id=current_user.id,
        topic=topic,
        score=score,
        total=total
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return {"message": "Score saved successfully", "score_id": db_score.id}

@router.get("/student-scores/{user_id}")
def get_student_scores(user_id: int, db: Session = Depends(get_db)):
    scores = db.query(StudentScore).filter(StudentScore.user_id == user_id).order_by(StudentScore.timestamp.desc()).all()
    
    return {
        "scores": [
            {
                "topic": score.topic,
                "score": score.score,
                "total": score.total,
                "timestamp": score.timestamp.isoformat()
            }
            for score in scores
        ]
    }
