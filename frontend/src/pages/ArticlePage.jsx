import { useParams } from "react-router-dom";
import { useOutletContext } from "react-router-dom";
import { useEffect, useState } from "react";

import Header from "../components/layout/Header";

import ArticleDetail from "../components/articles/ArticleDetail";
import {
  ArticleDetailSkeleton,
} from "../components/articles/ArticleSkeleton";

import ErrorState from "../components/common/ErrorState";

import { getArticle } from "../api/articles";

export default function ArticlePage() {
  const { articleId } = useParams();

  const { openSidebar } =
    useOutletContext() || {};

  const [article, setArticle] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  async function loadArticle() {
    try {
      setLoading(true);
      setError("");

      const data = await getArticle(
        articleId
      );

      setArticle(data);
    } catch (err) {
      setError(
        err.message ||
          "Failed to load article"
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadArticle();
  }, [articleId]);

  return (
    <>
      <Header
        title="Article Intelligence"
        subtitle="Detailed context from the NewsLens corpus."
        onMenuClick={openSidebar}
      />

      <div className="page-content narrow-content">
        {error ? (
          <ErrorState
            message={error}
            onRetry={loadArticle}
          />
        ) : loading ? (
          <ArticleDetailSkeleton />
        ) : article ? (
          <ArticleDetail article={article} />
        ) : null}
      </div>
    </>
  );
}