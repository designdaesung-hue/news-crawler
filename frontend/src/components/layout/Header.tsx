import { triggerCrawl } from "@/api/news";
import { useState } from "react";

export function Header() {
  const [crawling, setCrawling] = useState(false);

  const handleCrawl = async () => {
    setCrawling(true);
    try {
      await triggerCrawl();
      alert("크롤링이 시작되었습니다.");
    } finally {
      setCrawling(false);
    }
  };

  return (
    <header style={{ padding: "16px 24px", borderBottom: "1px solid #e5e7eb", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
      <h1 style={{ margin: 0, fontSize: "1.4rem", fontWeight: 700 }}>뉴스 크롤러</h1>
      <button onClick={handleCrawl} disabled={crawling}>
        {crawling ? "크롤링 중..." : "지금 크롤링"}
      </button>
    </header>
  );
}
