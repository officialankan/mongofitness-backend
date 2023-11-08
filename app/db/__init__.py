from app.db.database_manager import DatabaseManager
from app.db.mongo_manager import MongoManager

db = MongoManager()

async def get_database() -> MongoManager:
    return db
