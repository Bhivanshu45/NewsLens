import api from "./client";

export async function triggerIngestion() {
  return api.post("/api/v1/news/ingest");
}