import {
  ArrowLeft,
  ExternalLink,
  Layers3,
  CalendarDays,
  Database,
} from "lucide-react";

import { Link } from "react-router-dom";

import SourceBadge from "../common/SourceBadge";

import {
  formatDateTime,
  cleanText,
} from "../../utils/formatter.js";

export default function ArticleDetail({
  article,
}) {
  const content = cleanText(
    article.content || ""
  );

  return (
    <article className="article-detail">
      <Link
        to="/articles"
        className="back-link"
      >
        <ArrowLeft size={15} />
        Back to news
      </Link>

      <div className="detail-topline">
        <SourceBadge source={article.source} />

        <span className="detail-date">
          <CalendarDays size={14} />
          {formatDateTime(article.published_at)}
        </span>
      </div>

      <h1>{article.title}</h1>

      {article.summary && (
        <div className="article-lead">
          {article.summary}
        </div>
      )}

      <div className="detail-actions">
        <a
          href={article.url}
          target="_blank"
          rel="noreferrer"
          className="button button-primary"
        >
          <ExternalLink size={16} />
          Read original
        </a>

        {article.cluster_id && (
          <Link
            to={`/clusters/${article.cluster_id}`}
            className="button button-secondary"
          >
            <Layers3 size={16} />
            Explore topic
          </Link>
        )}
      </div>

      <div className="article-content">
        <div className="content-heading">
          <Database size={16} />
          Article content
        </div>

        {content ? (
          content
            .split(/\n+/)
            .filter(Boolean)
            .map((paragraph, index) => (
              <p key={index}>
                {paragraph}
              </p>
            ))
        ) : (
          <p className="muted">
            Full article content is not available.
            Use the original source above to continue
            reading.
          </p>
        )}
      </div>

      <div className="article-record">
        <span>
          NewsLens record #{article.id}
        </span>

        <span>
          Added {formatDateTime(article.created_at)}
        </span>
      </div>
    </article>
  );
}