import api from "./client";

export async function getArticles({
  page = 1,
  limit = 20,
  source = "",
} = {}) {
  const params = new URLSearchParams({
    page: String(page),
    limit: String(limit),
  });

  if (source) {
    params.set("source", source);
  }

  return api.get(`/api/v1/articles?${params.toString()}`);
}

export async function getArticle(articleId) {
  return api.get(`/api/v1/articles/${articleId}`);
}

export async function searchArticles({
  query,
  page = 1,
  limit = 20,
}) {
  const params = new URLSearchParams({
    q: query,
    page: String(page),
    limit: String(limit),
  });

  return api.get(`/api/v1/articles/search?${params.toString()}`);
}

export async function semanticSearch({
  query,
  limit = 10,
}) {
  const params = new URLSearchParams({
    q: query,
    limit: String(limit),
  });

  return api.get(`/api/v1/articles/semantic-search?${params.toString()}`);
}