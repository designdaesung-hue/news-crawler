from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.models.news import SourceName


@dataclass
class RawArticle:
    title: str
    url: str
    summary: Optional[str] = None
    image_url: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    content: Optional[str] = None


class BaseCrawler(ABC):
    source_name: SourceName
    display_name: str
    base_url: str

    @abstractmethod
    async def fetch(self, max_articles: int = 50) -> list[RawArticle]:
        """Fetch articles from the source and return raw article data."""
        ...

    async def fetch_content(self, url: str) -> Optional[str]:
        """Optionally fetch full article content from a detail page."""
        return None
