from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.conf.config import get_database_settings
from app.db.database_manager import DatabaseManager
from datetime import datetime, date, timezone, timedelta
import pandas as pd
import numpy as np
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
        cursor = self.db["polar"].aggregate([
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
        cursor = self.db["polar"].aggregate([
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
        cursor = self.db["polar"].aggregate([
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
    
    async def get_longest_streak(self, threshold: int):
        logging.info(f"Getting longest streak with {threshold} steps...")
        steps = await self.get_daily_steps()
        if not steps:
            raise HTTPException(status_code=404, detail="No daily steps found")
        # transform to dataframe to resample to daily and fill with nan
        df = pd.DataFrame(steps)
        df = df.set_index(pd.to_datetime(df["ts"]))
        s = df["steps"].resample("1D").asfreq()
        s = s >= threshold

        # https://stackoverflow.com/questions/4494404/find-large-number-of-consecutive-values-fulfilling-condition-in-a-numpy-array
        arr = s.values
        y = arr[1:] != arr[:-1] 
        i = np.append(np.nonzero(y)[0], arr.size - 1)
        rl = np.diff(np.append(-1, i))  # streak lengths
        pos = np.cumsum(np.append(0, rl))[:-1]  # positions
        return np.max(rl * arr[pos].T)  # only look at True streaks

    async def get_activity_type_by_range(self, start: date, end: date):
        logging.info(f"Getting activity type(s) from {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}...")
        cursor = self.db["strava"].aggregate([
            {
                '$match': {
                    'start_date': {
                        '$gte': datetime(start.year, start.month, start.day, tzinfo=timezone.utc), 
                        '$lt': datetime(end.year, end.month, end.day, tzinfo=timezone.utc)
                    }
                }
            }, 
            {
                '$group': {
                    '_id': {
                        '$dayOfYear': '$start_date'
                    }, 
                    'dt': {
                        '$first': '$start_date'
                    }, 
                    'sport_type': {
                        '$push': '$sport_type'
                    }
                }
            }, 
            {
                '$project': {
                    '_id': 0, 
                    'ts': {
                        '$dateFromParts': {
                            'year': {
                                '$year': '$dt'
                            }, 
                            'month': {
                                '$month': '$dt'
                            }, 
                            'day': {
                                '$dayOfMonth': '$dt'
                            }
                        }
                    }, 
                    'sport_type': 1
                }
            }, 
            {
                '$sort': {
                    'ts': 1
                }
            }
        ])
        activity_type = await cursor.to_list(length=None)
        if not activity_type:
            raise HTTPException(status_code=404, detail=f"No activity type(s) found from {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
        return activity_type
