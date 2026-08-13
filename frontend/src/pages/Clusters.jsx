import {
  useOutletContext,
} from "react-router-dom";

import Header from "../components/layout/Header";
import ClusterGrid from "../components/clusters/ClusterGrid";

import {
  Skeleton,
} from "../components/common/LoadingSkeleton";

import ErrorState from "../components/common/ErrorState";

import {
  useClusters,
} from "../hooks/useClusters";

export default function Clusters() {
  const { openSidebar } =
    useOutletContext() || {};

  const {
    clusters,
    loading,
    error,
    refetch,
  } = useClusters();

  return (
    <>
      <Header
        title="Topics"
        subtitle="See the stories people are talking about."
        onMenuClick={openSidebar}
        onRefresh={refetch}
        refreshing={loading}
      />

      <div className="page-content">
        <section className="news-page-heading">
          <div>
            <span className="eyebrow">
              TOPICS
            </span>

            <h2>
              What's being talked about
            </h2>

            <p>
              Related stories are grouped together so
              you can follow a topic from different
              sources.
            </p>
          </div>
        </section>

        <div className="results-heading">
          <div>
            <span className="eyebrow">
              DISCOVER
            </span>

            <h3>
              Popular topics
            </h3>
          </div>

          <span className="result-count">
            {clusters.length} topics
          </span>
        </div>

        {error ? (
          <ErrorState
            message={error}
            onRetry={refetch}
          />
        ) : loading ? (
          <div className="cluster-grid">
            {Array.from({
              length: 6,
            }).map((_, index) => (
              <div
                className="cluster-card"
                key={index}
              >
                <Skeleton className="skeleton-line small" />
                <Skeleton className="skeleton-line title" />
                <Skeleton className="skeleton-line body" />
                <Skeleton className="skeleton-line body short" />
              </div>
            ))}
          </div>
        ) : (
          <ClusterGrid
            clusters={clusters}
          />
        )}
      </div>
    </>
  );
}