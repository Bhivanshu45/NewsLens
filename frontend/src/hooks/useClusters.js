import { useCallback, useEffect, useState } from "react";
import { getCluster, getClusters } from "../api/clusters";

export function useClusters() {
  const [clusters, setClusters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchClusters = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getClusters();

      setClusters(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message || "Failed to load topics");
      setClusters([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchClusters();
  }, [fetchClusters]);

  return {
    clusters,
    loading,
    error,
    refetch: fetchClusters,
  };
}

export function useCluster(clusterId) {
  const [cluster, setCluster] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchCluster = useCallback(async () => {
    if (!clusterId) {
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError("");

      const data = await getCluster(clusterId);

      setCluster(data);
    } catch (err) {
      setError(err.message || "Failed to load topic");
      setCluster(null);
    } finally {
      setLoading(false);
    }
  }, [clusterId]);

  useEffect(() => {
    fetchCluster();
  }, [fetchCluster]);

  return {
    cluster,
    loading,
    error,
    refetch: fetchCluster,
  };
}