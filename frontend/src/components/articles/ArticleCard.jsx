import {
  ArrowUpRight,
  ExternalLink,
} from "lucide-react";

import { Link } from "react-router-dom";

import SourceBadge from "../common/SourceBadge";

import {
  timeAgo,
  truncate,
} from "../../utils/formatter.js";

export default function ArticleCard({
  article,
  featured = false,
}) {
  return (
    <article
      className={`article-card ${
        featured
          ? "article-card-featured"
          : ""
      }`}
    >
      <div className="article-card-top">
        <SourceBadge source={article.source} />

        <span className="article-time">
          {timeAgo(article.published_at)}
        </span>
      </div>

      <Link
        to={`/articles/${article.id}`}
        className="article-title"
      >
        {article.title}
      </Link>

      <p className="article-summary">
        {truncate(
          article.summary ||
            article.content ||
            "No summary available.",
          featured ? 280 : 180
        )}
      </p>

      <div className="article-card-footer">
        {article.cluster_id ? (
          <Link
            to={`/clusters/${article.cluster_id}`}
            className="cluster-link"
          >
            <span>
              More on this story
            </span>
          </Link>
        ) : (
          <span className="article-meta">
            {article.source}
          </span>
        )}

        <div className="article-card-actions">
          <a
            href={article.url}
            target="_blank"
            rel="noreferrer"
            className="external-link"
            title="Read original story"
          >
            <ExternalLink size={15} />
          </a>

          <Link
            to={`/articles/${article.id}`}
            className="article-open"
          >
            <ArrowUpRight size={15} />
          </Link>
        </div>
      </div>
    </article>
  );
}