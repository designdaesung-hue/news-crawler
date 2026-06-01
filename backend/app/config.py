from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "News Crawler API"
    debug: bool = False

    # Database
    database_url: str = "sqlite+aiosqlite:///./news.db"

    # Crawling
    crawl_interval_minutes: int = 30
    crawl_max_articles_per_source: int = 50
    request_timeout_seconds: int = 30

    # CORS — 배포 시 ALLOWED_ORIGINS=["*"] 또는 Vercel URL로 설정
    allowed_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    allow_all_origins: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
