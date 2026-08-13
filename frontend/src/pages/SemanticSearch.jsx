import {
  Search,
} from "lucide-react";

import {
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
import EmptyState from "../components/common/EmptyState";

import {
  useArticles,
} from "../hooks/useArticles";

const examples = [
  "AI companies raising funding",
  "global markets and economic news",
  "new developments in space",
  "recent cybersecurity incidents",
];

export default function SemanticSearch() {
  const { openSidebar } =
    useOutletContext() || {};

  const [query, setQuery] =
    useState("");

  const [
    submittedQuery,
    setSubmittedQuery,
  ] = useState("");

  const {
    articles,
    loading,
    error,
    refetch,
  } = useArticles({
    query: submittedQuery,
    mode: "semantic",
    limit: 10,
  });

  function submit() {
    if (!query.trim()) return;

    setSubmittedQuery(
      query.trim()
    );
  }

  function clear() {
    setQuery("");
    setSubmittedQuery("");
  }

  return (
    <>
      <Header
        title="Search"
        subtitle="Find stories using your own words."
        onMenuClick={openSidebar}
      />

      <div className="page-content">
        <section className="search-hero">
          <Search size={25} />

          <span className="eyebrow">
            FIND A STORY
          </span>

          <h2>
            What would you like to read?
          </h2>

          <p>
            Search for a topic, event, person or
            story. NewsLens will find the most relevant
            articles for you.
          </p>

          <SearchBar
            value={query}
            onChange={setQuery}
            onSubmit={submit}
            onClear={clear}
            semantic
            placeholder="Try “news about AI funding”..."
          />

          <div className="search-examples">
            {examples.map((example) => (
              <button
                key={example}
                onClick={() => {
                  setQuery(example);
                  setSubmittedQuery(
                    example
                  );
                }}
              >
                {example}
              </button>
            ))}
          </div>
        </section>

        {submittedQuery ? (
          <>
            <div className="results-heading">
              <div>
                <span className="eyebrow">
                  SEARCH RESULTS
                </span>

                <h3>
                  Stories related to “
                  {submittedQuery}”
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
              <GridSkeleton count={6} />
            ) : (
              <ArticleGrid
                articles={articles}
              />
            )}
          </>
        ) : (
          <EmptyState
            icon={Search}
            title="Search the news"
            description="Type what you are looking for and NewsLens will find related stories."
          />
        )}
      </div>
    </>
  );
}