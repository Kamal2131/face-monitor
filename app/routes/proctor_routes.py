# app/routes/proctor_routes.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.auth import get_current_username
from app.database import get_db
from app.models import ProctorEvent

router = APIRouter()

class ProctorEventIn(BaseModel):
    reason: str
    timestamp: str

class ProctorBatch(BaseModel):
    events: List[ProctorEventIn]

@router.post("/api/proctor/events")
async def proctor_events(
    batch: ProctorBatch,
    user: str = Depends(get_current_username),  # Assuming this returns the username
    db: Session = Depends(get_db)
):
    print("Received batch:", batch.json())
    print("Current user:", user)
    saved = 0

    for evt in batch.events:
        ts_str = evt.timestamp
        if ts_str.endswith("Z"):
            ts_str = ts_str[:-1] + "+00:00"
        try:
            ts = datetime.fromisoformat(ts_str)
        except Exception as e:
            print(f"Timestamp parsing error for '{evt.timestamp}':", e)
            return JSONResponse(status_code=400, content={"error": f"Invalid timestamp '{evt.timestamp}'"})

        pe = ProctorEvent(user_id=user, reason=evt.reason, timestamp=ts)
        db.add(pe)
        saved += 1

    try:
        db.commit()
    except Exception as e:
        print("DB commit error:", e)
        return JSONResponse(status_code=500, content={"error": "Database error"})

    return {"status": "ok", "saved": saved}
