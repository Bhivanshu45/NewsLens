import { useParams } from "react-router-dom";
import { useOutletContext } from "react-router-dom";

import Header from "../components/layout/Header";

import ClusterDetail from "../components/clusters/ClusterDetail";

import ErrorState from "../components/common/ErrorState";

import {
  useCluster,
} from "../hooks/useClusters";

import {
  Skeleton,
} from "../components/common/LoadingSkeleton";

export default function ClusterPage() {
  const { clusterId } = useParams();

  const { openSidebar } =
    useOutletContext() || {};

  const {
    cluster,
    loading,
    error,
    refetch,
  } = useCluster(clusterId);

  return (
    <>
      <Header
        title="Topic Intelligence"
        subtitle="Explore the stories connected to this topic."
        onMenuClick={openSidebar}
        onRefresh={refetch}
        refreshing={loading}
      />

      <div className="page-content">
        {error ? (
          <ErrorState
            message={error}
            onRetry={refetch}
          />
        ) : loading ? (
          <div className="article-detail">
            <Skeleton className="skeleton-line small" />
            <Skeleton className="skeleton-line hero-title" />
            <Skeleton className="skeleton-line hero-title short" />
            <Skeleton className="detail-block" />
          </div>
        ) : cluster ? (
          <ClusterDetail cluster={cluster} />
        ) : null}
      </div>
    </>
  );
}