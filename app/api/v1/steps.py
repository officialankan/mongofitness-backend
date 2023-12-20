from fastapi import APIRouter, Depends
from app.db.database_manager import DatabaseManager
from app.db import get_database
from app.db.models import DailySteps
from typing import List
from datetime import date

router = APIRouter()

@router.get("/")
async def get_daily_steps(db: DatabaseManager = Depends(get_database)) -> List[DailySteps]:
    """Get daily steps."""
    return await db.get_daily_steps()

@router.get("/{day}")
async def get_daily_steps_by_date(day: date, db: DatabaseManager = Depends(get_database)) -> DailySteps:
    """Get daily steps by date."""
    return await db.get_daily_steps_by_date(day)

@router.get("/range/")
async def get_daily_steps_by_range(start: date, end: date, db: DatabaseManager = Depends(get_database)) -> List[DailySteps]:
    """Get daily steps by date range."""
    return await db.get_daily_steps_by_range(start, end)

@router.get("/streak/")
async def get_longest_streak(threshold: int, db: DatabaseManager = Depends(get_database)) -> int:
    """Get longest daily steps streak based on a threshold."""
    return await db.get_longest_streak(threshold)
