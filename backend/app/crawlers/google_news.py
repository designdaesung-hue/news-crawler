from datetime import datetime

import httpx
from bs4 import BeautifulSoup

from app.crawlers.base import BaseCrawler, RawArticle
from app.models.news import SourceName


class GoogleNewsCrawler(BaseCrawler):
    source_name = SourceName.GOOGLE_NEWS
    display_name = "Google 뉴스"
    base_url = "https://news.google.com"

    # Google News RSS — no JS rendering required
    RSS_URL = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"

    async def fetch(self, max_articles: int = 50) -> list[RawArticle]:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(self.RSS_URL)
            resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml-xml")
        items = soup.find_all("item")[:max_articles]

        articles: list[RawArticle] = []
        for item in items:
            title = item.find("title")
            link = item.find("link")
            pub_date = item.find("pubDate")
            description = item.find("description")

            if not title or not link:
                continue

            published_at = None
            if pub_date and pub_date.text:
                try:
                    from email.utils import parsedate_to_datetime
                    published_at = parsedate_to_datetime(pub_date.text)
                except Exception:
                    pass

            articles.append(
                RawArticle(
                    title=title.text.strip(),
                    url=link.text.strip() if link.text else link.get("href", ""),
                    summary=BeautifulSoup(description.text, "html.parser").get_text() if description else None,
                    published_at=published_at,
                )
            )

        return articles
