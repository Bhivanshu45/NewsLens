import {
  ArrowUpRight,
} from "lucide-react";

import { Link } from "react-router-dom";

import {
  truncate,
} from "../../utils/formatter.js";

export default function TrendingTopics({
  clusters,
}) {
  return (
    <section className="dashboard-panel">
      <div className="panel-header">
        <div>
          <span className="eyebrow">
            TRENDING
          </span>

          <h2>Topics people are following</h2>
        </div>

        <Link
          to="/clusters"
          className="panel-link"
        >
          See all
          <ArrowUpRight size={14} />
        </Link>
      </div>

      <div className="topic-list">
        {clusters.slice(0, 6).map(
          (cluster, index) => (
            <Link
              to={`/clusters/${cluster.id}`}
              key={cluster.id}
              className="topic-row"
            >
              <span className="topic-index">
                {String(index + 1).padStart(2, "0")}
              </span>

              <div className="topic-info">
                <strong>
                  {cluster.title}
                </strong>

                <span>
                  {truncate(
                    cluster.summary ||
                      "Latest stories related to this topic.",
                    100
                  )}
                </span>
              </div>

              <ArrowUpRight size={15} />
            </Link>
          )
        )}

        {!clusters.length && (
          <div className="panel-empty">
            No trending topics yet.
          </div>
        )}
      </div>
    </section>
  );
}