import { useCallback, useEffect, useState } from "react";

import {
  getArticles,
  searchArticles,
  semanticSearch,
} from "../api/articles";

export function useArticles({
  page = 1,
  limit = 20,
  source = "",
  query = "",
  mode = "latest",
}) {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchArticles = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      let data;

      if (mode === "search" && query.trim()) {
        data = await searchArticles({
          query: query.trim(),
          page,
          limit,
        });
      } else if (mode === "semantic" && query.trim()) {
        data = await semanticSearch({
          query: query.trim(),
          limit,
        });
      } else {
        data = await getArticles({
          page,
          limit,
          source,
        });
      }

      setArticles(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message || "Failed to load articles");
      setArticles([]);
    } finally {
      setLoading(false);
    }
  }, [page, limit, source, query, mode]);

  useEffect(() => {
    fetchArticles();
  }, [fetchArticles]);

  return {
    articles,
    loading,
    error,
    refetch: fetchArticles,
  };
}