import { create } from "zustand";
import type { ArticleFilters, Category, SourceName } from "@/types/news";

interface FilterState extends ArticleFilters {
  setCategory: (category: Category | undefined) => void;
  setSource: (source: SourceName | undefined) => void;
  setQuery: (q: string) => void;
  setPage: (page: number) => void;
  reset: () => void;
}

export const useFilterStore = create<FilterState>((set) => ({
  page: 1,
  page_size: 20,
  category: undefined,
  source: undefined,
  q: undefined,

  setCategory: (category) => set({ category, page: 1 }),
  setSource: (source) => set({ source, page: 1 }),
  setQuery: (q) => set({ q: q || undefined, page: 1 }),
  setPage: (page) => set({ page }),
  reset: () => set({ page: 1, category: undefined, source: undefined, q: undefined }),
}));
