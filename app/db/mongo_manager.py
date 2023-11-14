from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.conf.config import get_database_settings
from app.db.database_manager import DatabaseManager
from datetime import datetime, date, timezone
import logging
from fastapi import HTTPException

db_settings = get_database_settings()

class MongoManager(DatabaseManager):
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self):
        logging.info("Connecting to database...")
        self.client = AsyncIOMotorClient(db_settings.dsn,
                                         maxPoolSize=10,
                                         minPoolSize=10)
        self.db = self.client[db_settings.database]
        logging.info("Connected to database.")

    async def close_database_connection(self):
        logging.info("Closing database connection...")
        self.client.close()
        logging.info("Closed database connection.")
    
    async def get_daily_steps(self):
        logging.info("Getting daily steps...")
        cursor = self.db[db_settings.collection].aggregate([
            {
                '$sort': {
                    'steps': -1
                }
            }, 
            {
                '$group': {
                    '_id': {
                        '$dayOfYear': '$ts'
                    }, 
                    'ts': {
                        '$first': '$ts'
                    }, 
                    'steps': {
                        '$first': '$steps'
                    }
                }
            }, 
            {
                '$project': {
                    '_id': 0
                }, 
            }, 
            {
                '$sort': {
                    'ts': 1
                }
            }
        ])
        daily_steps = await cursor.to_list(length=None)
        if not daily_steps:
            raise HTTPException(status_code=404, detail="No daily steps found")
        return daily_steps

    async def get_daily_steps_by_date(self, day: date):
        logging.info("Getting daily steps for {date.strftime('%Y-%m-%d')}...")
        cursor = self.db[db_settings.collection].aggregate([
                {
                    "$match": {
                        "ts": datetime(day.year, day.month, day=day.day, tzinfo=timezone.utc)
                    }
                }, 
                {
                    "$sort": {
                        "steps": -1
                    }
                }, 
                {
                    "$limit": 1
                }, 
                {
                    '$project': {
                        '_id': 0, 
                        'ts': 1, 
                        'steps': 1
                    }
                }
            ])
        daily_steps = await cursor.to_list(length=1)
        if not daily_steps:
            raise HTTPException(status_code=404, detail=f"No daily steps found for {day.strftime('%Y-%m-%d')}")
        return daily_steps[0]

    async def get_daily_steps_by_range(self, start: date, end: date):
        logging.info(f"Getting daily steps from {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}...")
        cursor = self.db[db_settings.collection].aggregate([
            {
                '$match': {
                    'ts': {
                        '$gte': datetime(start.year, start.month, start.day, tzinfo=timezone.utc), 
                        '$lte': datetime(end.year, end.month, end.day, tzinfo=timezone.utc)
                    }
                }
            }, 
            {
                '$sort': {
                    'steps': -1
                }
            }, 
            {
                '$group': {
                    '_id': {
                        '$dayOfYear': '$ts'
                    }, 
                    'ts': {
                        '$first': '$ts'
                    }, 
                    'steps': {
                        '$first': '$steps'
                    }
                }
            }, 
            {
                '$project': {
                    '_id': 0
                }, 
            }, 
            {
                '$sort': {
                    'ts': 1
                }
            }
        ])
        daily_steps = await cursor.to_list(length=None)
        if not daily_steps:
            raise HTTPException(status_code=404, detail=f"No daily steps found from {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
        return daily_steps
