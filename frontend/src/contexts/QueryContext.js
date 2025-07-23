import React, { createContext, useContext, useState } from 'react';

const QueryContext = createContext();

export const QueryProvider = ({ children }) => {
  const [queryHistory, setQueryHistory] = useState([]);
  
  const addQuery = (query) => {
    setQueryHistory(prev => [query, ...prev].slice(0, 10));
  };

  const value = {
    queryHistory,
    addQuery
  };

  return (
    <QueryContext.Provider value={value}>
      {children}
    </QueryContext.Provider>
  );
};

// Export the useQuery hook that your components are expecting
export const useQuery = () => {
  const context = useContext(QueryContext);
  if (!context) {
    throw new Error('useQuery must be used within a QueryProvider');
  }
  return context;
};

// Keep the alias for compatibility
export const useQueryContext = useQuery;

export default QueryContext;
