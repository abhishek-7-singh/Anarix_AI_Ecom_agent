import { useState, useCallback } from 'react';
import { queryAPI } from '../../../src/services/api';

export const useQuery = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const submitQuery = useCallback(async (question, options = {}) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await queryAPI.submitQuery(question, options);
      setResult(result);
      return result;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Query failed';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const submitStreamingQuery = useCallback(async (question, onChunk) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await queryAPI.submitStreamingQuery(question);
      
      // Handle streaming response
      const reader = response.data.getReader();
      const decoder = new TextDecoder();
      let result = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        result += chunk;
        
        if (onChunk) {
          onChunk(chunk);
        }
      }

      setResult({ response: result });
      return result;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Streaming query failed';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const clearResult = useCallback(() => {
    setResult(null);
    setError(null);
  }, []);

  return {
    loading,
    error,
    result,
    submitQuery,
    submitStreamingQuery,
    clearResult,
  };
};

export default useQuery;
