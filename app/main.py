from fastapi import FastAPI
from app.api import steps
from app.db import db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect_to_database()
    yield
    await db.close_database_connection()
    
app = FastAPI(lifespan=lifespan)
app.include_router(steps.router, prefix="/api/v1/steps", tags=["steps"])
