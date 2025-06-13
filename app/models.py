from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role          = Column(String, default="student", nullable=False)  # Add this line ✅
    image_url     = Column(String)

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
