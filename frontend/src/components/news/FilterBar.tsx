import { CATEGORY_LABELS, SOURCE_LABELS } from "@/types/news";
import type { Category, SourceName } from "@/types/news";
import { useFilterStore } from "@/store/filterStore";

const CATEGORIES = Object.entries(CATEGORY_LABELS) as [Category, string][];
const SOURCES = Object.entries(SOURCE_LABELS) as [SourceName, string][];

export function FilterBar() {
  const { category, source, q, setCategory, setSource, setQuery, reset } = useFilterStore();

  return (
    <div style={{ display: "flex", gap: "12px", flexWrap: "wrap", padding: "12px 24px", borderBottom: "1px solid #e5e7eb" }}>
      <input
        type="text"
        placeholder="검색어 입력..."
        value={q ?? ""}
        onChange={(e) => setQuery(e.target.value)}
        style={{ padding: "6px 12px", borderRadius: 6, border: "1px solid #d1d5db" }}
      />

      <select value={category ?? ""} onChange={(e) => setCategory((e.target.value as Category) || undefined)}>
        <option value="">전체 카테고리</option>
        {CATEGORIES.map(([val, label]) => (
          <option key={val} value={val}>{label}</option>
        ))}
      </select>

      <select value={source ?? ""} onChange={(e) => setSource((e.target.value as SourceName) || undefined)}>
        <option value="">전체 언론사</option>
        {SOURCES.map(([val, label]) => (
          <option key={val} value={val}>{label}</option>
        ))}
      </select>

      <button onClick={reset}>초기화</button>
    </div>
  );
}
