from app.crawlers.google_news import GoogleNewsCrawler
from app.crawlers.naver_news import NaverNewsCrawler
from app.crawlers.chosun import ChosunCrawler
from app.crawlers.joongang import JoongangCrawler
from app.crawlers.hani import HaniCrawler
from app.crawlers.yonhap import YonhapCrawler

ALL_CRAWLERS = [
    GoogleNewsCrawler,
    NaverNewsCrawler,
    ChosunCrawler,
    JoongangCrawler,
    HaniCrawler,
    YonhapCrawler,
]
