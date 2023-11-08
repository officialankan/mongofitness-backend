from fastapi import APIRouter, Depends
from app.db.database_manager import DatabaseManager
from app.db import get_database
from app.db.models import DailySteps
from datetime import date
from typing import List

router = APIRouter()

@router.get("/{from_str}")
async def get_daily_steps(from_str: date, to_str: date | None = None, 
                          db: DatabaseManager = Depends(get_database)) -> DailySteps | List[DailySteps]:
    """Get daily steps from a given date to a given date.
    
    If only one date is given, then the daily steps for that date is returned. Use the
     `to_str` query parameter to get the daily steps for a range of dates.
    """
    return await db.get_daily_steps(from_str, to_str)
