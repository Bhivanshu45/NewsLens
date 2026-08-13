import {
  ArrowLeft,
  ArrowUpRight,
  Newspaper,
} from "lucide-react";

import { Link } from "react-router-dom";

import ArticleCard from "../articles/ArticleCard";

import {
  formatDate,
} from "../../utils/formatter.js";

export default function ClusterDetail({
  cluster,
}) {
  return (
    <div className="cluster-detail">
      <Link
        to="/clusters"
        className="back-link"
      >
        <ArrowLeft size={15} />
        Back to topics
      </Link>

      <div className="cluster-hero">
        <div>
          <div className="eyebrow">
            TOPIC
          </div>

          <h1>{cluster.title}</h1>

          <span className="detail-date">
            Updated {formatDate(cluster.created_at)}
          </span>
        </div>
      </div>

      {cluster.summary && (
        <div className="cluster-summary">
          <div className="summary-label">
            About this topic
          </div>

          <p>{cluster.summary}</p>
        </div>
      )}

      <div className="section-heading-row">
        <div>
          <div className="eyebrow">
            RELATED STORIES
          </div>

          <h2>
            Latest stories on this topic
          </h2>
        </div>

        <Newspaper size={19} />
      </div>

      {cluster.articles?.length ? (
        <div className="article-grid">
          {cluster.articles.map((article) => (
            <ArticleCard
              key={article.id}
              article={article}
            />
          ))}
        </div>
      ) : (
        <div className="muted">
          No related stories available.
        </div>
      )}
    </div>
  );
}