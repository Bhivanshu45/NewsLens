import api from "./client";

export async function getHealth() {
  return api.get("/api/v1/health");
}