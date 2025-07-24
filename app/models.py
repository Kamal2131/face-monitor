from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from .database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="student")
    student_id = Column(String, nullable=True)
    course = Column(String, nullable=True)
    total_score = Column(Integer, default=0)  # Used for leaderboard ranking


class ProctorEvent(Base):
    __tablename__ = 'proctor_events'
    id        = Column(Integer, primary_key=True, index=True)
    user_id   = Column(String, index=True, nullable=False)
    reason    = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)


class Question(Base):
    __tablename__ = "questions"

    id              = Column(Integer, primary_key=True, index=True)
    question_text   = Column(String, nullable=False)
    option1         = Column(String, nullable=False)
    option2         = Column(String, nullable=False)
    option3         = Column(String, nullable=False)
    option4         = Column(String, nullable=False)
    correct_option  = Column(Integer, nullable=False)  # Should be 1, 2, 3, or 4

class StudentScore(Base):
    __tablename__ = 'student_scores'

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False)
    topic      = Column(String, nullable=False)
    score      = Column(Float, nullable=False)
    total      = Column(Integer, nullable=False)  # ✅ Add this line
    timestamp  = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="scores")

