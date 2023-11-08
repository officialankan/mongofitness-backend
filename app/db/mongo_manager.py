from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.conf.config import get_database_settings
from app.db.database_manager import DatabaseManager
from app.db.models import DailySteps
from datetime import date, datetime, timezone
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
    
    async def get_daily_steps(self, from_str: date, to_str: date | None = None):
        if to_str:
            logging.info(f"Getting daily steps from {from_str} to {to_str}...")
            cursor = self.db[db_settings.collection].aggregate([
                {
                    '$match': {
                        'ts': {
                            '$gte': datetime(from_str.year, from_str.month, from_str.day, tzinfo=timezone.utc), 
                            '$lte': datetime(to_str.year, to_str.month, to_str.day, tzinfo=timezone.utc)
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
            if daily_steps:
                return daily_steps
            else:
                raise HTTPException(status_code=404, detail=f"Daily steps from {from_str} to {to_str} not found.")

        else:
            logging.info(f"Getting daily steps for {from_str}...")
            cursor = self.db[db_settings.collection].aggregate([
                {
                    "$match": {
                        "ts": datetime(from_str.year, from_str.month, from_str.day, tzinfo=timezone.utc)
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
            if daily_steps:
                return daily_steps[0]
            else:
                raise HTTPException(status_code=404, detail=f"Daily steps for {from_str} not found.")