from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.news import Article, Category, Source, SourceName
from app.schemas.news import ArticleOut, ArticleList, SourceOut
from app.scheduler.jobs import crawl_source, run_all_crawlers
from app.crawlers import ALL_CRAWLERS

router = APIRouter(prefix="/api", tags=["news"])


@router.get("/articles", response_model=ArticleList)
async def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[Category] = None,
    source: Optional[SourceName] = None,
    q: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Article).options(selectinload(Article.source))

    if category:
        query = query.where(Article.category == category)
    if source:
        query = query.join(Article.source).where(Source.name == source)
    if q:
        query = query.where(Article.title.contains(q))

    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_result.scalar_one()

    query = (
        query.order_by(Article.published_at.desc().nullslast(), Article.crawled_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    articles = result.scalars().all()

    return ArticleList(total=total, page=page, page_size=page_size, items=list(articles))


@router.get("/articles/{article_id}", response_model=ArticleOut)
async def get_article(article_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Article)
        .options(selectinload(Article.source))
        .where(Article.id == article_id)
    )
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.get("/sources", response_model=List[SourceOut])
async def list_sources(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Source))
    return result.scalars().all()


@router.post("/crawl", status_code=202)
async def trigger_crawl(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_all_crawlers)
    return {"message": "Crawl triggered"}


@router.post("/crawl/{source_name}", status_code=202)
async def trigger_crawl_source(source_name: SourceName, background_tasks: BackgroundTasks):
    crawler_class = next(
        (c for c in ALL_CRAWLERS if c.source_name == source_name), None
    )
    if not crawler_class:
        raise HTTPException(status_code=404, detail="Source not found")
    background_tasks.add_task(crawl_source, crawler_class)
    return {"message": f"Crawl triggered for {source_name}"}
