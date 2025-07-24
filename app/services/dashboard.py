from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app.models import StudentScore, User

def get_dashboard_data(db: Session, user: User):
    # Fetch all scores for the user
    scores = db.query(StudentScore).filter(StudentScore.user_id == user.id).all()

    if scores:
        total_score = sum(s.score for s in scores)
        total_marks = sum(s.total for s in scores)
        avg_score = round((total_score / total_marks) * 100, 1) if total_marks > 0 else 0.0  # type: ignore
    else:
        total_score = 0
        total_marks = 0
        avg_score = 0.0

    score_change = 4.2  # Stubbed
    exam_count = len(scores)

    # 🏆 Calculate Rank by total score
    user_totals = (
        db.query(StudentScore.user_id, func.sum(StudentScore.score).label("total"))
        .group_by(StudentScore.user_id)
        .order_by(desc("total"))
        .all()
    )
    rank = next((i + 1 for i, row in enumerate(user_totals) if row.user_id == user.id), None)

    # 📊 Recent Exams
    recent_exams = sorted(scores, key=lambda x: x.timestamp, reverse=True)[:4]  # type: ignore
    exams = [
        {
            "title": s.topic,
            "score": round(s.score),
            "total": s.total,
            "date": s.timestamp.strftime("%b %d, %Y")
        }
        for s in recent_exams
    ]

    return {
        "user": {
            "name": user.name,
            "student_id": user.student_id,
            "department": user.course,
        },
        "avg_score": avg_score,
        "score_change": score_change,
        "exam_count": exam_count,
        "total_score": total_score,
        "total_marks": total_marks,
        "rank": rank,
        "next_exam": {
            "title": "Operating Systems Quiz",
            "date": (datetime.utcnow() + timedelta(days=5)).strftime("%b %d, %Y")
        },
        "next_exam_days": 5,
        "current_course": "Algorithm Analysis",
        "streak": 28,
        "progress_percent": 75,  # Optional to remove if unused
        "exams": exams
    }
