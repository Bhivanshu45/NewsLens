import api from "./client";

export async function getClusters() {
  return api.get("/api/v1/clusters");
}

export async function getCluster(clusterId) {
  return api.get(`/api/v1/clusters/${clusterId}`);
}
