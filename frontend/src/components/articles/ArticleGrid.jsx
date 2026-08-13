import ArticleCard from "./ArticleCard";

import EmptyState from "../common/EmptyState";

import { Newspaper } from "lucide-react";

export default function ArticleGrid({
  articles,
  featuredFirst = false,
}) {
  if (!articles?.length) {
    return (
      <EmptyState
        icon={Newspaper}
        title="No articles found"
        description="Try another search or refresh the intelligence feed."
      />
    );
  }

  return (
    <div className="article-grid">
      {articles.map((article, index) => (
        <ArticleCard
          key={article.id}
          article={article}
          featured={featuredFirst && index === 0}
        />
      ))}
    </div>
  );
}