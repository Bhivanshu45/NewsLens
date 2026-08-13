import {
  Bot,
  Search,
} from "lucide-react";

import {
  Link,
  useOutletContext,
} from "react-router-dom";

import Header from "../components/layout/Header";

import IntelligenceStats from "../components/dashboard/IntelligenceStats";
import TrendingTopics from "../components/dashboard/TrendingTopics";
import LatestNews from "../components/dashboard/LatestNews";

import {
  useArticles,
} from "../hooks/useArticles";

import {
  useClusters,
} from "../hooks/useClusters";

import {
  GridSkeleton,
} from "../components/common/LoadingSkeleton";

import ErrorState from "../components/common/ErrorState";

export default function Dashboard() {
  const { openSidebar } =
    useOutletContext() || {};

  const {
    articles,
    loading: articlesLoading,
    error: articlesError,
    refetch: refetchArticles,
  } = useArticles({
    limit: 20,
  });

  const {
    clusters,
    loading: clustersLoading,
    error: clustersError,
    refetch: refetchClusters,
  } = useClusters();

  const loading =
    articlesLoading || clustersLoading;

  function refresh() {
    refetchArticles();
    refetchClusters();
  }

  return (
    <>
      <Header
        title="NewsLens"
        subtitle="Stay informed. Search what matters."
        onMenuClick={openSidebar}
        onRefresh={refresh}
        refreshing={loading}
      />

      <div className="page-content">
        <section className="news-home-hero">
          <div>
            <span className="eyebrow">
              TODAY'S NEWS
            </span>

            <h2>
              Know what's happening.
            </h2>

            <p>
              Read the latest stories from across
              different sources, discover what's
              trending, or ask NewsLens about a story.
            </p>

            <div className="hero-actions">
              <Link
                to="/articles"
                className="button button-primary"
              >
                <Search size={16} />
                Browse news
              </Link>

              <Link
                to="/chat"
                className="button button-secondary"
              >
                <Bot size={16} />
                Ask NewsLens
              </Link>
            </div>
          </div>
        </section>

        {articlesError && (
          <ErrorState
            message={articlesError}
            onRetry={refresh}
          />
        )}

        {clustersError && (
          <ErrorState
            message={clustersError}
            onRetry={refresh}
          />
        )}

        {loading ? (
          <GridSkeleton count={6} />
        ) : (
          <>
            <IntelligenceStats
              articles={articles}
              clusters={clusters}
            />

            <div className="dashboard-two-column">
              <LatestNews
                articles={articles}
              />

              <TrendingTopics
                clusters={clusters}
              />
            </div>
          </>
        )}
      </div>
    </>
  );
}