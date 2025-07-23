export const API_ENDPOINTS = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  QUERY: '/query',
  QUERY_STREAM: '/query/stream',
  QUERY_EXAMPLES: '/query/examples',
  METRICS_SUMMARY: '/metrics/summary',
  METRICS_PERFORMANCE: '/metrics/performance',
  METRICS_TRENDS: '/metrics/trends',
  HEALTH: '/health',
  SQL_EXECUTE: '/sql/execute',
};

export const CHART_TYPES = {
  BAR: 'bar',
  PIE: 'pie',
  LINE: 'line',
  SCATTER: 'scatter',
};

export const CHART_COLORS = [
  '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
  '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
  '#F8C471', '#82E0AA', '#AED6F1', '#F7DC6F', '#D7BDE2',
];

export const METRICS_LABELS = {
  total_sales: 'Total Sales',
  total_ad_spend: 'Total Ad Spend',
  total_roas: 'Return on Ad Spend',
  eligible_products: 'Eligible Products',
  total_products: 'Total Products',
  conversion_rate: 'Conversion Rate',
  cpc: 'Cost Per Click',
  ctr: 'Click-Through Rate',
};

export const CURRENCY_FORMAT = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
});

export const NUMBER_FORMAT = new Intl.NumberFormat('en-US');

export const PERCENTAGE_FORMAT = new Intl.NumberFormat('en-US', {
  style: 'percent',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

export const DATE_FORMAT_OPTIONS = {
  year: 'numeric',
  month: 'short',
  day: 'numeric',
};

export const EXAMPLE_QUERIES = [
  "What is my total sales?",
  "Calculate the Return on Ad Spend (ROAS)",
  "Which product had the highest CPC (Cost Per Click)?",
  "Show me the top 10 products by revenue",
  "What's the conversion rate by product?",
  "How many products are eligible for advertising?",
  "What's my total ad spend this month?",
  "Which products have the best ROAS?",
  "Show me products with zero sales",
  "What's the average order value?",
];

export const LOADING_MESSAGES = [
  "Analyzing your data...",
  "Processing your request...",
  "Generating insights...",
  "Calculating metrics...",
  "Preparing your results...",
];

export const ERROR_MESSAGES = {
  NETWORK_ERROR: "Unable to connect to the server. Please check your connection.",
  TIMEOUT_ERROR: "Request timed out. Please try again.",
  SERVER_ERROR: "Server error occurred. Please try again later.",
  VALIDATION_ERROR: "Invalid input. Please check your query.",
  NOT_FOUND: "Requested resource not found.",
  GENERIC_ERROR: "An unexpected error occurred. Please try again.",
};

export const SUCCESS_MESSAGES = {
  QUERY_SUCCESS: "Query executed successfully!",
  DATA_LOADED: "Data loaded successfully!",
  EXPORT_SUCCESS: "Data exported successfully!",
};

export const ANIMATION_DURATIONS = {
  FAST: 200,
  NORMAL: 300,
  SLOW: 500,
  CHART_TRANSITION: 1000,
};

export const BREAKPOINTS = {
  mobile: '(max-width: 767px)',
  tablet: '(min-width: 768px) and (max-width: 1023px)',
  desktop: '(min-width: 1024px)',
};

export const THEME_COLORS = {
  primary: '#1976d2',
  secondary: '#dc004e',
  success: '#2e7d32',
  warning: '#ed6c02',
  error: '#d32f2f',
  info: '#0288d1',
};
