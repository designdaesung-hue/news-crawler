import { useQuery } from "@tanstack/react-query";
import { fetchArticles, fetchSources } from "@/api/news";
import type { ArticleFilters } from "@/types/news";

export function useArticles(filters: ArticleFilters) {
  return useQuery({
    queryKey: ["articles", filters],
    queryFn: () => fetchArticles(filters),
    placeholderData: (prev) => prev,
  });
}

export function useSources() {
  return useQuery({
    queryKey: ["sources"],
    queryFn: fetchSources,
    staleTime: 60_000,
  });
}
