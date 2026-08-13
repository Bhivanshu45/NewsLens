import {
  Search,
  SlidersHorizontal,
} from "lucide-react";

import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  useOutletContext,
} from "react-router-dom";

import Header from "../components/layout/Header";
import SearchBar from "../components/articles/SearchBar";
import ArticleGrid from "../components/articles/ArticleGrid";

import {
  GridSkeleton,
} from "../components/common/LoadingSkeleton";

import ErrorState from "../components/common/ErrorState";

import {
  useArticles,
} from "../hooks/useArticles";

export default function Articles() {
  const { openSidebar } =
    useOutletContext() || {};

  const [query, setQuery] =
    useState("");

  const [submittedQuery, setSubmittedQuery] =
    useState("");

  const [page, setPage] =
    useState(1);

  const [source, setSource] =
    useState("");

  const mode = submittedQuery
    ? "search"
    : "latest";

  const {
    articles,
    loading,
    error,
    refetch,
  } = useArticles({
    page,
    limit: 20,
    source,
    query: submittedQuery,
    mode,
  });

  const sources = useMemo(
    () =>
      [
        ...new Set(
          articles
            .map(
              (article) =>
                article.source
            )
            .filter(Boolean)
        ),
      ],
    [articles]
  );

  useEffect(() => {
    setPage(1);
  }, [submittedQuery, source]);

  function submitSearch() {
    setPage(1);
    setSubmittedQuery(query.trim());
  }

  function clearSearch() {
    setQuery("");
    setSubmittedQuery("");
    setPage(1);
  }

  return (
    <>
      <Header
        title="Latest News"
        subtitle="Read the latest stories from your news sources."
        onMenuClick={openSidebar}
        onRefresh={refetch}
        refreshing={loading}
      />

      <div className="page-content">
        <section className="news-page-heading">
          <div>
            <span className="eyebrow">
              NEWS
            </span>

            <h2>
              {submittedQuery
                ? `Search results`
                : "Latest stories"}
            </h2>

            <p>
              {submittedQuery
                ? `Stories matching “${submittedQuery}”.`
                : "Fresh stories collected and summarized for you."}
            </p>
          </div>

          <Search size={24} />
        </section>

        <div className="search-section">
          <SearchBar
            value={query}
            onChange={setQuery}
            onSubmit={submitSearch}
            onClear={clearSearch}
            placeholder="Search news..."
          />

          <div className="filter-row">
            <div className="filter-label">
              <SlidersHorizontal size={14} />
              Sources
            </div>

            <button
              className={`filter-chip ${
                !source
                  ? "filter-chip-active"
                  : ""
              }`}
              onClick={() =>
                setSource("")
              }
            >
              All
            </button>

            {sources.map((item) => (
              <button
                key={item}
                className={`filter-chip ${
                  source === item
                    ? "filter-chip-active"
                    : ""
                }`}
                onClick={() =>
                  setSource(item)
                }
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        <div className="results-heading">
          <div>
            <span className="eyebrow">
              {submittedQuery
                ? "RESULTS"
                : "LATEST"}
            </span>

            <h3>
              {submittedQuery
                ? `Stories for “${submittedQuery}”`
                : "Recent news"}
            </h3>
          </div>

          <span className="result-count">
            {articles.length} stories
          </span>
        </div>

        {error ? (
          <ErrorState
            message={error}
            onRetry={refetch}
          />
        ) : loading ? (
          <GridSkeleton count={8} />
        ) : (
          <ArticleGrid
            articles={articles}
          />
        )}

        {!loading &&
          !error &&
          articles.length > 0 && (
            <div className="pagination">
              <button
                disabled={page === 1}
                onClick={() =>
                  setPage((current) =>
                    Math.max(
                      1,
                      current - 1
                    )
                  )
                }
              >
                Previous
              </button>

              <span>
                Page {page}
              </span>

              <button
                disabled={
                  articles.length < 20
                }
                onClick={() =>
                  setPage(
                    (current) =>
                      current + 1
                  )
                }
              >
                Next
              </button>
            </div>
          )}
      </div>
    </>
  );
}