from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.news import Category, SourceName


class SourceOut(BaseModel):
    id: int
    name: SourceName
    display_name: str
    base_url: str
    is_active: bool
    last_crawled_at: Optional[datetime]

    model_config = {"from_attributes": True}


class ArticleOut(BaseModel):
    id: int
    title: str
    url: str
    summary: Optional[str]
    image_url: Optional[str]
    author: Optional[str]
    category: Category
    published_at: Optional[datetime]
    crawled_at: datetime
    source: SourceOut

    model_config = {"from_attributes": True}


class ArticleList(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[ArticleOut]
