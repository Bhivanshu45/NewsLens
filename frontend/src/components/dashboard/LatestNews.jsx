import {
  ArrowUpRight,
  Newspaper,
} from "lucide-react";

import { Link } from "react-router-dom";

import SourceBadge from "../common/SourceBadge";

import {
  timeAgo,
  truncate,
} from "../../utils/formatter.js";

export default function LatestNews({
  articles,
}) {
  return (
    <section className="dashboard-panel">
      <div className="panel-header">
        <div>
          <span className="eyebrow">
            LATEST
          </span>

          <h2>What's happening now</h2>
        </div>

        <Link
          to="/articles"
          className="panel-link"
        >
          See all news
          <ArrowUpRight size={14} />
        </Link>
      </div>

      <div className="latest-list">
        {articles.slice(0, 7).map(
          (article) => (
            <Link
              to={`/articles/${article.id}`}
              key={article.id}
              className="latest-row"
            >
              <div className="latest-time">
                {timeAgo(
                  article.published_at
                )}
              </div>

              <div className="latest-main">
                <SourceBadge
                  source={article.source}
                />

                <strong>
                  {article.title}
                </strong>

                <p>
                  {truncate(
                    article.summary ||
                      article.content ||
                      "",
                    145
                  )}
                </p>
              </div>

              <ArrowUpRight
                size={16}
                className="latest-arrow"
              />
            </Link>
          )
        )}

        {!articles.length && (
          <div className="panel-empty">
            <Newspaper size={17} />
            No stories available.
          </div>
        )}
      </div>
    </section>
  );
}