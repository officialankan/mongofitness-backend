from fastapi import APIRouter, Depends
from app.db.database_manager import DatabaseManager
from app.db import get_database
from app.db.models import ActivityType
from typing import List
from datetime import date

router = APIRouter()

@router.get("/type/date/{day}")
async def get_activity_type_by_date(day: date, db: DatabaseManager = Depends(get_database)) -> List[ActivityType]:
    """Get activity type by date."""
    return await db.get_activity_type_by_date(day)
