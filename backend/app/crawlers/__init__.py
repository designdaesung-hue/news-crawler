from app.crawlers.google_news import GoogleNewsCrawler
from app.crawlers.naver_news import NaverNewsCrawler
from app.crawlers.joongang import JoongangCrawler
from app.crawlers.hani import HaniCrawler

ALL_CRAWLERS = [
    GoogleNewsCrawler,
    NaverNewsCrawler,
    JoongangCrawler,
    HaniCrawler,
]
