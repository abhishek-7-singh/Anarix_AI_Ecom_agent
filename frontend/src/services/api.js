import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
export const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`Response from ${response.config.url}:`, response.status);
    return response;
  },
  (error) => {
    console.error('Response error:', error.response?.data || error.message);
    
    if (error.response?.status === 500) {
      throw new Error('Server error. Please try again later.');
    } else if (error.response?.status === 404) {
      throw new Error('API endpoint not found. Please check your backend configuration.');
    } else if (error.response?.status === 400) {
      throw new Error(error.response.data?.detail || 'Invalid request.');
    } else if (error.code === 'ECONNABORTED') {
      throw new Error('Request timeout. Please try again.');
    }
    
    return Promise.reject(error);
  }
);

// API methods with FIXED endpoints
export const queryAPI = {
  // Submit natural language query - FIXED PATH
  submitQuery: async (question, options = {}) => {
    const response = await apiClient.post('/api/query', {  // Added /api prefix
      question,
      stream: options.stream || false,
      include_chart: options.include_chart !== false,
    });
    return response.data;
  },

  // Get example queries - FIXED PATH
  getExampleQueries: async () => {
    const response = await apiClient.get('/api/query/examples');  // Added /api prefix
    return response.data.examples;
  },

  // Execute raw SQL - FIXED PATH
  executeSQL: async (sqlQuery) => {
    const response = await apiClient.post('/api/sql/execute', {  // Added /api prefix
      sql_query: sqlQuery,
    });
    return response.data;
  },
};

export const metricsAPI = {
  // Get summary metrics - FIXED PATH
  getSummary: async () => {
    const response = await apiClient.get('/api/metrics/summary');  // Added /api prefix
    return response.data;
  },

  // Get performance metrics - FIXED PATH
  getPerformance: async () => {
    const response = await apiClient.get('/api/metrics/performance');  // Added /api prefix
    return response.data;
  },

  // Get trend data - FIXED PATH
  getTrends: async () => {
    const response = await apiClient.get('/api/metrics/trends');  // Added /api prefix
    return response.data;
  },

  // Get product-specific metrics - FIXED PATH
  getProductMetrics: async (itemId) => {
    const response = await apiClient.get(`/api/metrics/products/${itemId}`);  // Added /api prefix
    return response.data;
  },
};

export const healthAPI = {
  // Basic health check - CORRECT PATH (no /api prefix needed)
  checkHealth: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },

  // Detailed health check - CORRECT PATH (no /api prefix needed)
  checkDetailedHealth: async () => {
    const response = await apiClient.get('/health/detailed');
    return response.data;
  },
};

export default apiClient;
