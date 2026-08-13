import {
  ArrowLeft,
  SearchX,
} from "lucide-react";

import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="not-found">
      <div className="not-found-icon">
        <SearchX size={27} />
      </div>

      <span className="eyebrow">
        404
      </span>

      <h1>
        Intelligence not found.
      </h1>

      <p>
        The page you are looking for does not exist
        in the NewsLens workspace.
      </p>

      <Link
        to="/dashboard"
        className="button button-primary"
      >
        <ArrowLeft size={16} />
        Return to dashboard
      </Link>
    </div>
  );
}