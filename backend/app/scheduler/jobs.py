import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from app.config import settings
from app.crawlers import ALL_CRAWLERS
from app.database import AsyncSessionLocal
from app.models.news import Article, Source
from app.utils.category import classify_category

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


async def crawl_source(crawler_class) -> int:
    crawler = crawler_class()
    saved = 0

    try:
        raw_articles = await crawler.fetch(
            max_articles=settings.crawl_max_articles_per_source
        )
    except Exception as e:
        logger.error(f"[{crawler.display_name}] fetch failed: {e}")
        return 0

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Source).where(Source.name == crawler.source_name)
        )
        source = result.scalar_one_or_none()
        if not source:
            source = Source(
                name=crawler.source_name,
                display_name=crawler.display_name,
                base_url=crawler.base_url,
            )
            db.add(source)
            await db.flush()

        for raw in raw_articles:
            exists = await db.execute(
                select(Article).where(Article.url == raw.url)
            )
            if exists.scalar_one_or_none():
                continue

            category = classify_category(raw.title, raw.summary or "")
            article = Article(
                source_id=source.id,
                title=raw.title,
                url=raw.url,
                summary=raw.summary,
                image_url=raw.image_url,
                author=raw.author,
                category=category,
                published_at=raw.published_at,
            )
            db.add(article)
            saved += 1

        source.last_crawled_at = datetime.utcnow()
        await db.commit()

    logger.info(f"[{crawler.display_name}] saved {saved} new articles")
    return saved


async def run_all_crawlers():
    logger.info("Starting scheduled crawl for all sources...")
    for crawler_class in ALL_CRAWLERS:
        await crawl_source(crawler_class)


def start_scheduler():
    scheduler.add_job(
        run_all_crawlers,
        trigger="interval",
        minutes=settings.crawl_interval_minutes,
        id="crawl_all",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(
        f"Scheduler started — crawling every {settings.crawl_interval_minutes} minutes"
    )


def stop_scheduler():
    scheduler.shutdown(wait=False)
