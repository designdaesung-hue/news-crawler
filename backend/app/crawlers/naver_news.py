from __future__ import annotations

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

# 뉴스 섹션 페이지 목록 (속보 + 주요 섹션)
SECTION_URLS = [
    "https://news.naver.com",
    "https://news.naver.com/section/100",  # 정치
    "https://news.naver.com/section/101",  # 경제
    "https://news.naver.com/section/102",  # 사회
    "https://news.naver.com/section/105",  # IT/과학
]


class NaverNewsCrawler(BaseCrawler):
    source_name = SourceName.NAVER_NEWS
    display_name = "네이버 뉴스"
    base_url = "https://news.naver.com"

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
                    if "n.news.naver.com/article/" not in href:
                        continue
                    if href in seen_urls:
                        continue

                    # 제목: h4.cn_title 우선, 없으면 a 직계 텍스트
                    title_tag = a.find(class_="cn_title") or a.find("h4") or a.find("h3") or a.find("strong")
                    title = title_tag.get_text(strip=True) if title_tag else a.get_text(strip=True)
                    if not title:
                        continue

                    # 요약: cn_body 또는 description 클래스
                    summary_tag = a.find(class_=lambda c: c and any(
                        x in c for x in ["body", "summary", "desc", "snippet"]
                    ))
                    summary = summary_tag.get_text(strip=True) if summary_tag else None

                    # 이미지: 부모 컨테이너에서 탐색
                    parent = a.find_parent(["li", "div", "article", "section"])
                    img = parent.find("img") if parent else None
                    image_url = img.get("src") if img else None

                    seen_urls.add(href)
                    articles.append(
                        RawArticle(
                            title=title,
                            url=href,
                            summary=summary,
                            image_url=image_url,
                        )
                    )

                    if len(articles) >= max_articles:
                        break

        return articles
