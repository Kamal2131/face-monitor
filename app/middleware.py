from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from app.auth import get_current_user
from app.database import get_db  # this is your dependency
from sqlalchemy.orm import Session

async def auth_middleware(request: Request, call_next):
    if request.url.path.startswith(("/recognize", "/dashboard", "/api")):
        # Manually resolve the database session
        db_gen = get_db()
        db: Session = next(db_gen)
        try:
            user = get_current_user(request, db)  # pass db to get_current_user
            if user is None:
                return RedirectResponse("/login")
        except HTTPException:
            return RedirectResponse("/login")
        finally:
            db.close()

    return await call_next(request)
