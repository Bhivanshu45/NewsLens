import {
  ArrowUpRight,
} from "lucide-react";

import { Link } from "react-router-dom";

import {
  truncate,
} from "../../utils/formatter.js";

export default function ClusterCard({
  cluster,
  index,
}) {
  return (
    <Link
      to={`/clusters/${cluster.id}`}
      className="cluster-card"
    >
      <div className="cluster-card-header">
        <span className="cluster-number">
          {String(index + 1).padStart(2, "0")}
        </span>

        <span className="topic-label">
          Topic
        </span>
      </div>

      <h3>{cluster.title}</h3>

      <p>
        {truncate(
          cluster.summary ||
            "Stories and updates related to this topic.",
          180
        )}
      </p>

      <div className="cluster-card-footer">
        <span>
          Read related stories
        </span>

        <ArrowUpRight size={16} />
      </div>
    </Link>
  );
}