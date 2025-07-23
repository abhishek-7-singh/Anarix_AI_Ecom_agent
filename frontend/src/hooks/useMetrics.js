// import { useState, useEffect, useCallback } from 'react';
// import { metricsAPI } from '../../../src/services/api';

// export const useMetrics = () => {
//   const [metrics, setMetrics] = useState(null);
//   const [performance, setPerformance] = useState(null);
//   const [trends, setTrends] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   const loadSummary = useCallback(async () => {
//     setLoading(true);
//     setError(null);
    
//     try {
//       const data = await metricsAPI.getSummary();
//       setMetrics(data);
//       return data;
//     } catch (err) {
//       setError(err.message);
//       throw err;
//     } finally {
//       setLoading(false);
//     }
//   }, []);

//   const loadPerformance = useCallback(async () => {
//     setLoading(true);
//     setError(null);
    
//     try {
//       const data = await metricsAPI.getPerformance();
//       setPerformance(data);
//       return data;
//     } catch (err) {
//       setError(err.message);
//       throw err;
//     } finally {
//       setLoading(false);
//     }
//   }, []);

//   const loadTrends = useCallback(async () => {
//     setLoading(true);
//     setError(null);
    
//     try {
//       const data = await metricsAPI.getTrends();
//       setTrends(data);
//       return data;
//     } catch (err) {
//       setError(err.message);
//       throw err;
//     } finally {
//       setLoading(false);
//     }
//   }, []);

//   const loadProductMetrics = useCallback(async (itemId) => {
//     setLoading(true);
//     setError(null);
    
//     try {
//       const data = await metricsAPI.getProductMetrics(itemId);
//       return data;
//     } catch (err) {
//       setError(err.message);
//       throw err;
//     } finally {
//       setLoading(false);
//     }
//   }, []);

//   const refreshAll = useCallback(async () => {
//     try {
//       await Promise.all([
//         loadSummary(),
//         loadPerformance(),
//         loadTrends(),
//       ]);
//     } catch (err) {
//       console.error('Error refreshing metrics:', err);
//     }
//   }, [loadSummary, loadPerformance, loadTrends]);

//   // Auto-load summary metrics on mount
//   useEffect(() => {
//     loadSummary();
//   }, [loadSummary]);

//   return {
//     metrics,
//     performance,
//     trends,
//     loading,
//     error,
//     loadSummary,
//     loadPerformance,
//     loadTrends,
//     loadProductMetrics,
//     refreshAll,
//   };
// };

// export default useMetrics;
import { useState, useEffect, useCallback } from 'react';
import { metricsAPI } from '../services/api';  // Fixed import path

export const useMetrics = () => {
  const [metrics, setMetrics] = useState(null);
  const [performance, setPerformance] = useState(null);
  const [trends, setTrends] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadSummary = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await metricsAPI.getSummary();
      setMetrics(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const loadPerformance = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await metricsAPI.getPerformance();
      setPerformance(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const loadTrends = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await metricsAPI.getTrends();
      setTrends(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const loadProductMetrics = useCallback(async (itemId) => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await metricsAPI.getProductMetrics(itemId);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const refreshAll = useCallback(async () => {
    try {
      await Promise.all([
        loadSummary(),
        loadPerformance(),
        loadTrends(),
      ]);
    } catch (err) {
      console.error('Error refreshing metrics:', err);
    }
  }, [loadSummary, loadPerformance, loadTrends]);

  // Auto-load summary metrics on mount
  useEffect(() => {
    loadSummary();
  }, [loadSummary]);

  return {
    metrics,
    performance,
    trends,
    loading,
    error,
    loadSummary,
    loadPerformance,
    loadTrends,
    loadProductMetrics,
    refreshAll,
  };
};

export default useMetrics;
