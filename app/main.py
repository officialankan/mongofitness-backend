from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import steps, activities
from app.db import db
from contextlib import asynccontextmanager

origins = [
    "http://127.0.0.1:5173",
    "https://ankan-web.vercel.app"
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect_to_database()
    yield
    await db.close_database_connection()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(steps.router, prefix="/api/v1/steps", tags=["steps"])
app.include_router(activities.router, prefix="/api/v1/activities", tags=["activities"])
