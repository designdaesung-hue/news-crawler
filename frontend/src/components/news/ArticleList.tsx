import { useArticles } from "@/hooks/useArticles";
import { useFilterStore } from "@/store/filterStore";
import { ArticleCard } from "./ArticleCard";

export function ArticleList() {
  const filters = useFilterStore();
  const { data, isLoading, isError } = useArticles(filters);

  if (isLoading) return <p style={{ padding: 24 }}>불러오는 중...</p>;
  if (isError) return <p style={{ padding: 24, color: "red" }}>오류가 발생했습니다.</p>;
  if (!data || data.items.length === 0) return <p style={{ padding: 24, color: "#9ca3af" }}>기사가 없습니다.</p>;

  const { items, total, page, page_size, setPage } = { ...data, setPage: filters.setPage };
  const totalPages = Math.ceil(total / page_size);

  return (
    <div style={{ padding: 24 }}>
      <p style={{ margin: "0 0 16px", fontSize: "0.875rem", color: "#6b7280" }}>총 {total.toLocaleString()}건</p>

      {items.map((article) => (
        <ArticleCard key={article.id} article={article} />
      ))}

      {totalPages > 1 && (
        <div style={{ display: "flex", justifyContent: "center", gap: 8, marginTop: 24 }}>
          <button disabled={page <= 1} onClick={() => setPage(page - 1)}>이전</button>
          <span>{page} / {totalPages}</span>
          <button disabled={page >= totalPages} onClick={() => setPage(page + 1)}>다음</button>
        </div>
      )}
    </div>
  );
}
