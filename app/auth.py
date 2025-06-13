from fastapi import Request, HTTPException
import bcrypt
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    username = request.cookies.get("user")
    if not username:
        raise Exception("No user cookie found")
    
    user = db.query(User).filter_by(name=username).first()
    if not user:
        raise Exception("User not found in DB")
    print(f"Current user: {user.name}, Role: {user.role}")  # Debugging line to check user details
    return user  # ✅ returns full user object

def get_current_username(request: Request, db: Session = Depends(get_db)) -> User:
    username = request.cookies.get("user")
    if not username:
        raise Exception("No user cookie found")
    
    user = db.query(User).filter_by(name=username).first()
    if not user:
        raise Exception("User not found in DB")
    print(f"Current user: {user.name}, Role: {user.role}")  # Debugging line to check user details
    return user.name  # type: ignore # ✅ returns full user object

