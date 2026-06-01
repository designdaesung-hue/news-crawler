# 뉴스 크롤러

구글 뉴스, 네이버 뉴스, 조선일보, 중앙일보, 한겨레, 연합뉴스를 주기적으로 수집하고 카테고리별로 분류해 보여주는 웹 애플리케이션입니다.

## 기술 스택

| 영역 | 기술 |
|------|------|
| 백엔드 | Python 3.12, FastAPI, SQLAlchemy 2.0 |
| 크롤링 | httpx + BeautifulSoup4 (RSS), Playwright (JS 렌더링 옵션) |
| 스케줄링 | APScheduler |
| DB | SQLite (개발) / PostgreSQL (운영) |
| 프론트엔드 | React 18, TypeScript, Vite |
| 상태 관리 | TanStack Query + Zustand |

## 프로젝트 구조

```
news-crawler/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 앱 진입점
│   │   ├── config.py            # 환경변수 설정
│   │   ├── database.py          # DB 연결 / 세션
│   │   ├── models/              # SQLAlchemy 모델
│   │   ├── schemas/             # Pydantic 스키마
│   │   ├── api/routes/          # API 라우터
│   │   ├── crawlers/            # 언론사별 크롤러
│   │   ├── scheduler/           # APScheduler 작업
│   │   └── utils/               # 카테고리 분류 등
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/                 # axios API 클라이언트
│   │   ├── components/          # React 컴포넌트
│   │   ├── hooks/               # TanStack Query 훅
│   │   ├── store/               # Zustand 상태
│   │   └── types/               # TypeScript 타입
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

## 크롤링 대상

| 언론사 | 방식 | 비고 |
|--------|------|------|
| Google 뉴스 | RSS | `news.google.com/rss` |
| 네이버 뉴스 | RSS | `news.naver.com/rss` |
| 조선일보 | RSS | Arc 피드 |
| 중앙일보 | RSS | joins.com RSS |
| 한겨레 | RSS | `hani.co.kr/rss` |
| 연합뉴스 | RSS | `yna.co.kr/rss` |

## 카테고리 분류

키워드 기반 자동 분류 (`app/utils/category.py`):

- 정치 / 경제 / 사회 / 기술 / 국제 / 기타

## 빠른 시작

### 로컬 개발

```bash
# 백엔드
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
# → http://localhost:8000

# 프론트엔드 (새 터미널)
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

### Docker (개발)

```bash
cp .env.example .env
docker compose up --build
# 프론트: http://localhost
# API:    http://localhost:8000
# Swagger: http://localhost:8000/docs
```

### Docker (운영 — PostgreSQL 포함)

```bash
docker compose --profile prod up --build
```

## API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/articles` | 기사 목록 (필터: category, source, q, page) |
| GET | `/api/articles/{id}` | 기사 상세 |
| GET | `/api/sources` | 언론사 목록 |
| POST | `/api/crawl` | 전체 크롤링 즉시 실행 |
| POST | `/api/crawl/{source_name}` | 특정 언론사 크롤링 |
| GET | `/health` | 헬스체크 |

전체 API 문서: `http://localhost:8000/docs`

## 환경변수

`backend/.env.example` 참고:

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `DATABASE_URL` | SQLite | DB 연결 문자열 |
| `CRAWL_INTERVAL_MINUTES` | 30 | 자동 크롤링 주기 (분) |
| `CRAWL_MAX_ARTICLES_PER_SOURCE` | 50 | 언론사당 최대 수집 건수 |
| `DEBUG` | false | 디버그 모드 |

## Playwright 사용 (JS 렌더링 필요 시)

기본 크롤러는 RSS / httpx를 사용합니다.  
JS 렌더링이 필요한 사이트는 `BaseCrawler`의 `fetch()` 메서드에서 Playwright를 사용하도록 구현하세요.

```python
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.launch()
    page = await browser.new_page()
    await page.goto(url)
    html = await page.content()
    await browser.close()
```

Dockerfile에서 아래 주석을 해제하면 브라우저가 함께 설치됩니다:

```dockerfile
RUN playwright install --with-deps chromium
```
