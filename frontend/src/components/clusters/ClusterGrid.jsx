import { Layers3 } from "lucide-react";

import ClusterCard from "./ClusterCard";

import EmptyState from "../common/EmptyState";

export default function ClusterGrid({
  clusters,
}) {
  if (!clusters?.length) {
    return (
      <EmptyState
        icon={Layers3}
        title="No topics detected"
        description="Topics will appear as NewsLens groups related stories during ingestion."
      />
    );
  }

  return (
    <div className="cluster-grid">
      {clusters.map((cluster, index) => (
        <ClusterCard
          key={cluster.id}
          cluster={cluster}
          index={index}
        />
      ))}
    </div>
  );
}