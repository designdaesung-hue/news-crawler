import axios from "axios";
import type { Article, ArticleFilters, ArticleList, Source } from "@/types/news";

const BASE_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : "/api";

const api = axios.create({ baseURL: BASE_URL });

export async function fetchArticles(filters: ArticleFilters = {}): Promise<ArticleList> {
  const { data } = await api.get<ArticleList>("/articles", { params: filters });
  return data;
}

export async function fetchArticle(id: number): Promise<Article> {
  const { data } = await api.get<Article>(`/articles/${id}`);
  return data;
}

export async function fetchSources(): Promise<Source[]> {
  const { data } = await api.get<Source[]>("/sources");
  return data;
}

export async function triggerCrawl(): Promise<void> {
  await api.post("/crawl");
}
