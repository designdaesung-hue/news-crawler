export type Category =
  | "politics"
  | "economy"
  | "society"
  | "tech"
  | "international"
  | "uncategorized";

export type SourceName =
  | "google_news"
  | "naver_news"
  | "chosun"
  | "joongang"
  | "hani"
  | "yonhap";

export interface Source {
  id: number;
  name: SourceName;
  display_name: string;
  base_url: string;
  is_active: boolean;
  last_crawled_at: string | null;
}

export interface Article {
  id: number;
  title: string;
  url: string;
  summary: string | null;
  image_url: string | null;
  author: string | null;
  category: Category;
  published_at: string | null;
  crawled_at: string;
  source: Source;
}

export interface ArticleList {
  total: number;
  page: number;
  page_size: number;
  items: Article[];
}

export interface ArticleFilters {
  page?: number;
  page_size?: number;
  category?: Category;
  source?: SourceName;
  q?: string;
}

export const CATEGORY_LABELS: Record<Category, string> = {
  politics: "정치",
  economy: "경제",
  society: "사회",
  tech: "기술",
  international: "국제",
  uncategorized: "기타",
};

export const SOURCE_LABELS: Record<SourceName, string> = {
  google_news: "Google 뉴스",
  naver_news: "네이버 뉴스",
  chosun: "조선일보",
  joongang: "중앙일보",
  hani: "한겨레",
  yonhap: "연합뉴스",
};
