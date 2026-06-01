import { formatDistanceToNow } from "date-fns";
import { ko } from "date-fns/locale";
import type { Article } from "@/types/news";
import { CATEGORY_LABELS } from "@/types/news";

interface Props {
  article: Article;
}

export function ArticleCard({ article }: Props) {
  const timeAgo = article.published_at
    ? formatDistanceToNow(new Date(article.published_at), { addSuffix: true, locale: ko })
    : null;

  return (
    <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      style={{ textDecoration: "none", color: "inherit", display: "block", padding: "16px", border: "1px solid #e5e7eb", borderRadius: 8, marginBottom: 12, transition: "box-shadow .15s" }}
    >
      <div style={{ display: "flex", gap: "12px" }}>
        {article.image_url && (
          <img
            src={article.image_url}
            alt=""
            width={120}
            height={80}
            style={{ objectFit: "cover", borderRadius: 6, flexShrink: 0 }}
          />
        )}
        <div>
          <div style={{ display: "flex", gap: 8, marginBottom: 6, alignItems: "center" }}>
            <span style={{ fontSize: "0.75rem", background: "#f3f4f6", padding: "2px 8px", borderRadius: 4 }}>
              {CATEGORY_LABELS[article.category]}
            </span>
            <span style={{ fontSize: "0.75rem", color: "#6b7280" }}>{article.source.display_name}</span>
            {timeAgo && <span style={{ fontSize: "0.75rem", color: "#9ca3af" }}>{timeAgo}</span>}
          </div>
          <h3 style={{ margin: "0 0 6px", fontSize: "1rem", fontWeight: 600, lineHeight: 1.4 }}>{article.title}</h3>
          {article.summary && (
            <p style={{ margin: 0, fontSize: "0.875rem", color: "#6b7280", display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}>
              {article.summary}
            </p>
          )}
        </div>
      </div>
    </a>
  );
}
