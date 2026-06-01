from __future__ import annotations

import re

import httpx
from bs4 import BeautifulSoup

from app.crawlers.base import BaseCrawler, RawArticle
from app.models.news import SourceName

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

SECTION_URLS = [
    "https://www.joongang.co.kr/politics",
    "https://www.joongang.co.kr/money",
    "https://www.joongang.co.kr/society",
    "https://www.joongang.co.kr/international",
    "https://www.joongang.co.kr/culture",
]

ARTICLE_URL_RE = re.compile(r"joongang\.co\.kr/article/\d+")


class JoongangCrawler(BaseCrawler):
    source_name = SourceName.JOONGANG
    display_name = "중앙일보"
    base_url = "https://www.joongang.co.kr"

    async def fetch(self, max_articles: int = 50) -> list[RawArticle]:
        articles: list[RawArticle] = []
        seen_urls: set[str] = set()

        async with httpx.AsyncClient(
            headers=HEADERS, follow_redirects=True, timeout=30
        ) as client:
            for section_url in SECTION_URLS:
                if len(articles) >= max_articles:
                    break
                try:
                    resp = await client.get(section_url)
                    resp.raise_for_status()
                except Exception:
                    continue

                soup = BeautifulSoup(resp.text, "lxml")

                for a in soup.find_all("a", href=True):
                    href: str = a.get("href", "")
                    if not ARTICLE_URL_RE.search(href):
                        continue

                    # 절대 URL 정규화
                    if href.startswith("/"):
                        href = f"https://www.joongang.co.kr{href}"

                    if href in seen_urls:
                        continue

                    title = a.get_text(strip=True)
                    if not title:
                        continue

                    # 이미지: 부모 컨테이너에서 탐색
                    parent = a.find_parent(["li", "div", "article"])
                    img = parent.find("img") if parent else None
                    image_url = None
                    if img:
                        image_url = img.get("src") or img.get("data-src")

                    seen_urls.add(href)
                    articles.append(
                        RawArticle(
                            title=title,
                            url=href,
                            image_url=image_url,
                        )
                    )

                    if len(articles) >= max_articles:
                        break

        return articles
