from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

class ProctorEvent(Base):
    __tablename__ = 'proctor_events'
    id        = Column(Integer, primary_key=True, index=True)
    user_id   = Column(String, index=True, nullable=False)
    reason    = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
