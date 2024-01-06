from fastapi import APIRouter, Depends
from app.db.database_manager import DatabaseManager
from app.db import get_database
from app.db.models import ActivityTypeByDate
from typing import List
from datetime import date

router = APIRouter()

@router.get("/type/range/")
async def get_activitiy_type_by_range(start: date, end: date, db: DatabaseManager = Depends(get_database)) -> List[ActivityTypeByDate]:
    """Get activity type by date range."""
    return await db.get_activity_type_by_range(start, end)