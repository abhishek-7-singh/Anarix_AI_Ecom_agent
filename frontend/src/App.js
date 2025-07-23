
// import React, { useState, useEffect } from 'react';
// import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import { ThemeProvider } from '@mui/material/styles';
// import { 
//   CssBaseline, 
//   Container, 
//   Alert, 
//   Snackbar, 
//   Box,
//   Fade
// } from '@mui/material';

// import Navbar from './components/common/Header';
// import Dashboard from './components/dashboard/Dashboard';
// import QueryInterface from './components/query/QueryInterface';
// import ChartViewer from './components/charts/ChartViewer';
// import ErrorBoundary from './components/common/ErrorBoundary';
// import ParticleBackground from './components/common/ParticleBackground';

// import { QueryProvider } from './contexts/QueryContext';
// import { apiClient } from './services/api';
// import { theme } from './theme/theme';

// import './App.css';

// function App() {
//   const [currentView, setCurrentView] = useState('dashboard');
//   const [queryResult, setQueryResult] = useState(null);
//   const [error, setError] = useState(null);
//   const [healthStatus, setHealthStatus] = useState(null);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     checkHealth();
//     setTimeout(() => setLoading(false), 2000);
//   }, []);

//   const checkHealth = async () => {
//     try {
//       const health = await apiClient.get('/health');
//       setHealthStatus(health.data);
//     } catch (err) {
//       setError('API service is not available. Please check if the backend is running.');
//     }
//   };

//   const handleQueryResult = (result) => {
//     setQueryResult(result);
//     if (result.chart_data) {
//       setCurrentView('chart');
//     }
//   };

//   const handleError = (error) => {
//     setError(error);
//   };

//   const handleCloseError = () => {
//     setError(null);
//   };

//   if (loading) {
//     return (
//       <ThemeProvider theme={theme}>
//         <CssBaseline />
//         <Box 
//           sx={{ 
//             height: '100vh',
//             background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
//             display: 'flex',
//             alignItems: 'center',
//             justifyContent: 'center'
//           }}
//         >
//           <Box sx={{ textAlign: 'center' }}>
//             <Box
//               sx={{
//                 width: 80,
//                 height: 80,
//                 border: '3px solid rgba(255, 255, 255, 0.3)',
//                 borderTop: '3px solid #667eea',
//                 borderRadius: '50%',
//                 animation: 'spin 1s linear infinite',
//                 mx: 'auto',
//                 mb: 2,
//                 '@keyframes spin': {
//                   '0%': { transform: 'rotate(0deg)' },
//                   '100%': { transform: 'rotate(360deg)' },
//                 },
//               }}
//             />
//             <Box sx={{ 
//               fontSize: '1.5rem', 
//               fontWeight: 600, 
//               color: 'white',
//               mb: 1 
//             }}>
//               E-commerce AI Agent
//             </Box>
//             <Box sx={{ 
//               fontSize: '1rem', 
//               color: 'rgba(255, 255, 255, 0.7)' 
//             }}>
//               Initializing Mistral AI...
//             </Box>
//           </Box>
//         </Box>
//       </ThemeProvider>
//     );
//   }

//   return (
//     <ThemeProvider theme={theme}>
//       <CssBaseline />
//       <ErrorBoundary>
//         <QueryProvider>
//           <Router>
//             <Box 
//               sx={{ 
//                 minHeight: '100vh',
//                 background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
//                 position: 'relative',
//                 overflow: 'hidden'
//               }}
//             >
//               <ParticleBackground />
              
//               <Navbar 
//                 currentView={currentView} 
//                 setCurrentView={setCurrentView}
//                 healthStatus={healthStatus}
//               />
              
//               <Container maxWidth="xl" sx={{ pt: 4, pb: 4, position: 'relative', zIndex: 1 }}>
//                 <Fade in={true} timeout={1000}>
//                   <div>
//                     <Routes>
//                       <Route 
//                         path="/" 
//                         element={
//                           currentView === 'dashboard' ? (
//                             <Dashboard onError={handleError} />
//                           ) : currentView === 'query' ? (
//                             <QueryInterface 
//                               onResult={handleQueryResult}
//                               onError={handleError}
//                             />
//                           ) : currentView === 'chart' && queryResult ? (
//                             <ChartViewer 
//                               data={queryResult} 
//                               onBack={() => setCurrentView('query')}
//                             />
//                           ) : (
//                             <Dashboard onError={handleError} />
//                           )
//                         } 
//                       />
//                     </Routes>
//                   </div>
//                 </Fade>
//               </Container>

//               <Snackbar
//                 open={!!error}
//                 autoHideDuration={6000}
//                 onClose={handleCloseError}
//                 anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
//               >
//                 <Alert 
//                   onClose={handleCloseError} 
//                   severity="error" 
//                   sx={{ 
//                     width: '100%',
//                     background: 'rgba(211, 47, 47, 0.9)',
//                     backdropFilter: 'blur(10px)',
//                     border: '1px solid rgba(255, 255, 255, 0.2)',
//                     borderRadius: '15px'
//                   }}
//                 >
//                   {error}
//                 </Alert>
//               </Snackbar>
//             </Box>
//           </Router>
//         </QueryProvider>
//       </ErrorBoundary>
//     </ThemeProvider>
//   );
// }

// export default App;


import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { 
  CssBaseline, 
  Container, 
  Alert, 
  Snackbar, 
  Box,
  Fade
} from '@mui/material';

import Navbar from './components/common/Header';
import Dashboard from './components/dashboard/Dashboard';
import QueryInterface from './components/query/QueryInterface';
import ChartViewer from './components/charts/ChartViewer';
import ErrorBoundary from './components/common/ErrorBoundary';
import ParticleBackground from './components/common/ParticleBackground';

import { QueryProvider } from './contexts/QueryContext';
import { apiClient } from './services/api';
import { theme } from './theme/theme';

import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [queryResult, setQueryResult] = useState(null);
  const [error, setError] = useState(null);
  const [healthStatus, setHealthStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkHealth();
    setTimeout(() => setLoading(false), 2000);
  }, []);

  const checkHealth = async () => {
    try {
      const health = await apiClient.get('/health');
      setHealthStatus(health.data);
    } catch (err) {
      setError('API service is not available. Please check if the backend is running.');
    }
  };

  const handleQueryResult = (result) => {
    setQueryResult(result);
    if (result.chart_data) {
      setCurrentView('chart');
    }
  };

  const handleError = (error) => {
    setError(error);
  };

  const handleCloseError = () => {
    setError(null);
  };

  if (loading) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box 
          sx={{ 
            height: '100vh',
            background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <Box sx={{ textAlign: 'center' }}>
            <Box
              sx={{
                width: 80,
                height: 80,
                border: '3px solid rgba(255, 255, 255, 0.3)',
                borderTop: '3px solid #667eea',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite',
                mx: 'auto',
                mb: 2,
                '@keyframes spin': {
                  '0%': { transform: 'rotate(0deg)' },
                  '100%': { transform: 'rotate(360deg)' },
                },
              }}
            />
            <Box sx={{ 
              fontSize: '1.5rem', 
              fontWeight: 600, 
              color: 'white',
              mb: 1 
            }}>
              E-commerce AI Agent
            </Box>
            <Box sx={{ 
              fontSize: '1rem', 
              color: 'rgba(255, 255, 255, 0.7)' 
            }}>
              Initializing Mistral AI...
            </Box>
          </Box>
        </Box>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ErrorBoundary>
        <QueryProvider>
          <Router>
            <Box 
              sx={{ 
                minHeight: '100vh',
                background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                position: 'relative',
                overflow: 'hidden'
              }}
            >
              <ParticleBackground />
              
              <Navbar 
                currentView={currentView} 
                setCurrentView={setCurrentView}
                healthStatus={healthStatus}
              />
              
              <Container maxWidth="xl" sx={{ pt: 4, pb: 4, position: 'relative', zIndex: 1 }}>
                <Fade in={true} timeout={1000}>
                  <div>
                    <Routes>
                      <Route 
                        path="/" 
                        element={
                          currentView === 'dashboard' ? (
                            <Dashboard 
                              onError={handleError} 
                              setCurrentView={setCurrentView}  // ✅ ADDED
                            />
                          ) : currentView === 'query' ? (
                            <QueryInterface 
                              onResult={handleQueryResult}
                              onError={handleError}
                            />
                          ) : currentView === 'chart' && queryResult ? (
                            <ChartViewer 
                              data={queryResult} 
                              onBack={() => setCurrentView('query')}
                            />
                          ) : (
                            <Dashboard 
                              onError={handleError} 
                              setCurrentView={setCurrentView}  // ✅ ADDED
                            />
                          )
                        } 
                      />
                    </Routes>
                  </div>
                </Fade>
              </Container>

              <Snackbar
                open={!!error}
                autoHideDuration={6000}
                onClose={handleCloseError}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
              >
                <Alert 
                  onClose={handleCloseError} 
                  severity="error" 
                  sx={{ 
                    width: '100%',
                    background: 'rgba(211, 47, 47, 0.9)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    borderRadius: '15px'
                  }}
                >
                  {error}
                </Alert>
              </Snackbar>
            </Box>
          </Router>
        </QueryProvider>
      </ErrorBoundary>
    </ThemeProvider>
  );
}

export default App;
