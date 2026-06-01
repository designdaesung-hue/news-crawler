import pytest
from app.crawlers.google_news import GoogleNewsCrawler
from app.crawlers.yonhap import YonhapCrawler


@pytest.mark.asyncio
async def test_google_news_fetch():
    crawler = GoogleNewsCrawler()
    articles = await crawler.fetch(max_articles=5)
    assert isinstance(articles, list)
    if articles:
        assert articles[0].title
        assert articles[0].url


@pytest.mark.asyncio
async def test_yonhap_fetch():
    crawler = YonhapCrawler()
    articles = await crawler.fetch(max_articles=5)
    assert isinstance(articles, list)
