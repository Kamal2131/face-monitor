from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

from fastapi import HTTPException

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    username = request.cookies.get("user")
    if not username:
        raise HTTPException(status_code=401, detail="Please login to continue")
    
    user = db.query(User).filter_by(name=username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def get_current_username(request: Request, db: Session = Depends(get_db)) -> str:
    username = request.cookies.get("user")
    if not username:
        raise HTTPException(status_code=401, detail="Please login to continue")
    
    user = db.query(User).filter_by(name=username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    name = str(user.name)
    
    return name
