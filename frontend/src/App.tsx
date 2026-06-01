import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Header } from "@/components/layout/Header";
import { FilterBar } from "@/components/news/FilterBar";
import { ArticleList } from "@/components/news/ArticleList";

const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div style={{ maxWidth: 900, margin: "0 auto", fontFamily: "system-ui, sans-serif" }}>
        <Header />
        <FilterBar />
        <ArticleList />
      </div>
    </QueryClientProvider>
  );
}
