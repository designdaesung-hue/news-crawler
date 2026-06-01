from app.models.news import Category

POLITICS_KEYWORDS = [
    "정치", "국회", "대통령", "여당", "야당", "선거", "정당", "법안", "의원", "장관",
    "정부", "청와대", "용산", "국무", "총리", "대선", "총선",
]

ECONOMY_KEYWORDS = [
    "경제", "주식", "코스피", "환율", "금리", "부동산", "기업", "수출", "수입",
    "GDP", "물가", "인플레", "증시", "채권", "투자", "세금", "재정", "예산",
]

SOCIETY_KEYWORDS = [
    "사회", "교육", "의료", "복지", "노동", "범죄", "사고", "재난", "환경",
    "날씨", "문화", "스포츠", "연예", "건강", "인구", "출산",
]

TECH_KEYWORDS = [
    "기술", "IT", "AI", "인공지능", "반도체", "스마트폰", "앱", "소프트웨어",
    "플랫폼", "데이터", "클라우드", "메타버스", "로봇", "전기차", "배터리", "스타트업",
]

INTERNATIONAL_KEYWORDS = [
    "국제", "미국", "중국", "일본", "유럽", "러시아", "북한", "외교", "무역",
    "UN", "NATO", "전쟁", "분쟁", "협약", "조약", "글로벌",
]


def classify_category(title: str, content: str = "") -> Category:
    text = f"{title} {content}".lower()

    scores = {
        Category.POLITICS: sum(kw in text for kw in POLITICS_KEYWORDS),
        Category.ECONOMY: sum(kw in text for kw in ECONOMY_KEYWORDS),
        Category.SOCIETY: sum(kw in text for kw in SOCIETY_KEYWORDS),
        Category.TECH: sum(kw in text for kw in TECH_KEYWORDS),
        Category.INTERNATIONAL: sum(kw in text for kw in INTERNATIONAL_KEYWORDS),
    }

    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else Category.UNCATEGORIZED
