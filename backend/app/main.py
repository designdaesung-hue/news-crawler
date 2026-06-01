import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.news import router as news_router
from app.config import settings
from app.database import init_db
from app.scheduler.jobs import start_scheduler, stop_scheduler

logging.basicConfig(level=logging.INFO)

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news_router)


@app.on_event("startup")
async def on_startup():
    await init_db()
    start_scheduler()


@app.on_event("shutdown")
async def on_shutdown():
    stop_scheduler()


@app.get("/health")
async def health():
    return {"status": "ok"}
