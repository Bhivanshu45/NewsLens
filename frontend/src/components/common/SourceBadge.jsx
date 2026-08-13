import { Radio } from "lucide-react";

import { getInitials } from "../../utils/formatter.js";

export default function SourceBadge({
  source,
}) {
  return (
    <div className="source-badge">
      <span className="source-avatar">
        {getInitials(source)}
      </span>

      <span>{source}</span>
    </div>
  );
}