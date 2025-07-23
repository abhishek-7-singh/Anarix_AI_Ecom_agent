// import React, { useState, useEffect } from 'react';
// import { Card, CardContent, Typography, Grid, Box } from '@mui/material';
// import { apiClient } from '../../services/api';

// const Dashboard = ({ onError }) => {
//   const [metrics, setMetrics] = useState(null);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     loadMetrics();
//   }, []);

//   const loadMetrics = async () => {
//     try {
//       const response = await apiClient.get('/api/metrics/summary');
//       setMetrics(response.data);
//     } catch (error) {
//       onError('Failed to load metrics: ' + error.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   if (loading) return <Typography>Loading dashboard...</Typography>;

//   return (
//     <Box>
//       <Typography variant="h4" gutterBottom>
//         E-commerce Business Dashboard
//       </Typography>
      
//       <Grid container spacing={3}>
//         <Grid item xs={12} md={4}>
//           <Card>
//             <CardContent>
//               <Typography variant="h6">Total Sales</Typography>
//               <Typography variant="h4" color="primary">
//                 ${(metrics?.total_sales || 0).toLocaleString()}
//               </Typography>
//             </CardContent>
//           </Card>
//         </Grid>
        
//         <Grid item xs={12} md={4}>
//           <Card>
//             <CardContent>
//               <Typography variant="h6">Total Ad Spend</Typography>
//               <Typography variant="h4" color="secondary">
//                 ${(metrics?.total_ad_spend || 0).toLocaleString()}
//               </Typography>
//             </CardContent>
//           </Card>
//         </Grid>
        
//         <Grid item xs={12} md={4}>
//           <Card>
//             <CardContent>
//               <Typography variant="h6">ROAS</Typography>
//               <Typography variant="h4" color="success.main">
//                 {(metrics?.total_roas || 0).toFixed(2)}x
//               </Typography>
//             </CardContent>
//           </Card>
//         </Grid>
//       </Grid>
//     </Box>
//   );
// };

// export default Dashboard;
// src/components/dashboard/Dashboard.js
// src/components/dashboard/Dashboard.js
import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Box,
  Skeleton,
  Chip,
  LinearProgress,
  IconButton,
  Tooltip,
  Paper,
  Divider,
  Button,
  Alert,
  Fab
} from '@mui/material';
import {
  TrendingUp as SalesIcon,
  Campaign as AdIcon,
  Analytics as RoasIcon,
  Refresh as RefreshIcon,
  Timeline as TrendIcon,
  Assessment as AssessmentIcon,
  ShoppingCart as ProductIcon,
  Visibility as ViewIcon,
  GetApp as DownloadIcon,
  Psychology as AIIcon,
  AutoAwesome as SparkleIcon
} from '@mui/icons-material';
import { useMetrics } from '../../hooks/useMetrics';

const MetricCard = ({ title, value, subtitle, icon, color, trend, loading, unit = '' }) => (
  <Grid item xs={12} sm={6} md={4}>
    <Card 
      sx={{ 
        height: '100%',
        background: `linear-gradient(135deg, ${color}15 0%, ${color}25 100%)`,
        border: `1px solid ${color}30`,
        borderRadius: 4,
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        cursor: 'pointer',
        '&:hover': {
          transform: 'translateY(-8px) scale(1.02)',
          boxShadow: `0 20px 40px 0 ${color}25`,
          border: `1px solid ${color}50`,
        }
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Box
            sx={{
              p: 2,
              borderRadius: '16px',
              background: `${color}20`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: `0 4px 12px ${color}20`,
            }}
          >
            {icon}
          </Box>
          {trend && (
            <Chip
              icon={<TrendIcon sx={{ fontSize: 16 }} />}
              label={trend}
              size="small"
              sx={{ 
                background: trend.startsWith('+') ? 'rgba(76, 175, 80, 0.2)' : 'rgba(244, 67, 54, 0.2)',
                color: trend.startsWith('+') ? '#4caf50' : '#f44336',
                border: `1px solid ${trend.startsWith('+') ? '#4caf5050' : '#f4433650'}`,
                fontWeight: 600
              }}
            />
          )}
        </Box>
        
        <Typography variant="h6" sx={{ color: 'rgba(255, 255, 255, 0.8)', mb: 2, fontWeight: 500 }}>
          {title}
        </Typography>
        
        {loading ? (
          <Skeleton variant="text" width="80%" height={48} sx={{ bgcolor: 'rgba(255, 255, 255, 0.1)' }} />
        ) : (
          <Typography 
            variant="h3" 
            sx={{ 
              fontWeight: 800,
              mb: 1,
              fontSize: { xs: '1.8rem', sm: '2.2rem', md: '2.5rem' },
              background: `linear-gradient(45deg, ${color}, ${color}dd)`,
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              lineHeight: 1.2
            }}
          >
            {unit}{typeof value === 'number' ? value.toLocaleString() : value || '0'}
          </Typography>
        )}
        
        <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.6)', lineHeight: 1.4 }}>
          {subtitle}
        </Typography>
      </CardContent>
    </Card>
  </Grid>
);

const QuickActionCard = ({ title, description, icon, onClick, color }) => (
  <Card 
    sx={{ 
      height: '100%',
      background: 'rgba(255, 255, 255, 0.05)',
      backdropFilter: 'blur(10px)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      borderRadius: 3,
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      '&:hover': {
        background: 'rgba(255, 255, 255, 0.1)',
        transform: 'translateY(-4px)',
        boxShadow: '0 12px 24px rgba(0, 0, 0, 0.2)'
      }
    }}
    onClick={onClick}
  >
    <CardContent sx={{ p: 3, textAlign: 'center' }}>
      <Box sx={{ mb: 2 }}>
        {React.cloneElement(icon, { 
          sx: { fontSize: 32, color: color } 
        })}
      </Box>
      <Typography variant="h6" sx={{ color: 'white', mb: 1, fontWeight: 600 }}>
        {title}
      </Typography>
      <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
        {description}
      </Typography>
    </CardContent>
  </Card>
);

const Dashboard = ({ onError, setCurrentView }) => {
  const { metrics, loading, error, refreshAll } = useMetrics();
  const [lastRefresh, setLastRefresh] = useState(new Date());

  const handleRefresh = async () => {
    try {
      await refreshAll();
      setLastRefresh(new Date());
    } catch (err) {
      onError?.(err.message);
    }
  };

  const handleAskAI = () => {
    setCurrentView('query');
  };

  if (error) {
    return (
      <Box sx={{ mt: 8, mx: 2 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          Failed to load dashboard data: {error}
        </Alert>
        <Button variant="contained" onClick={handleRefresh}>
          Retry
        </Button>
      </Box>
    );
  }

  return (
    <Box sx={{ 
      mt: 8, 
      px: { xs: 2, sm: 3, md: 4 },
      pb: 4,
      minHeight: 'calc(100vh - 64px)'
    }}>
      {/* Header Section */}
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        mb: 6,
        flexDirection: { xs: 'column', sm: 'row' },
        gap: 2
      }}>
        <Box sx={{ textAlign: { xs: 'center', sm: 'left' } }}>
          <Typography 
            variant="h2" 
            sx={{
              fontSize: { xs: '2.5rem', sm: '3rem', md: '3.5rem' },
              fontWeight: 800,
              background: 'linear-gradient(45deg, #667eea, #764ba2)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              mb: 1,
              textShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}
          >
            Business Dashboard
          </Typography>
          <Typography 
            variant="h6" 
            sx={{ 
              color: 'rgba(255, 255, 255, 0.8)', 
              fontWeight: 400,
              maxWidth: 600
            }}
          >
            Real-time insights from your e-commerce data • 8,779+ records analyzed
          </Typography>
          <Typography 
            variant="body2" 
            sx={{ 
              color: 'rgba(255, 255, 255, 0.6)', 
              mt: 1,
              fontSize: '0.9rem'
            }}
          >
            Last updated: {lastRefresh.toLocaleTimeString()}
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          {/* Ask AI Button in Header */}
          <Button
            variant="contained"
            size="large"
            startIcon={<AIIcon />}
            onClick={handleAskAI}
            sx={{
              background: 'linear-gradient(45deg, #f093fb, #f5576c)',
              color: 'white',
              px: 3,
              py: 1.5,
              borderRadius: '25px',
              fontWeight: 600,
              fontSize: '1rem',
              boxShadow: '0 4px 16px rgba(240, 147, 251, 0.4)',
              transition: 'all 0.3s ease',
              '&:hover': {
                background: 'linear-gradient(45deg, #ed7ef8, #f04462)',
                transform: 'translateY(-2px)',
                boxShadow: '0 6px 20px rgba(240, 147, 251, 0.6)',
              }
            }}
          >
            Ask AI
          </Button>

          <Tooltip title="Refresh Data">
            <IconButton
              onClick={handleRefresh}
              disabled={loading}
              sx={{
                background: 'linear-gradient(45deg, #667eea, #764ba2)',
                color: 'white',
                width: 56,
                height: 56,
                boxShadow: '0 4px 16px rgba(102, 126, 234, 0.4)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #5a67d8, #6b46c1)',
                  transform: 'scale(1.05)',
                  boxShadow: '0 6px 20px rgba(102, 126, 234, 0.6)',
                },
                '&:disabled': {
                  background: 'rgba(255, 255, 255, 0.1)',
                  color: 'rgba(255, 255, 255, 0.5)'
                }
              }}
            >
              <RefreshIcon sx={{ fontSize: 28 }} />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* Main Metrics - Centered */}
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'center', 
        mb: 6 
      }}>
        <Box sx={{ width: '100%', maxWidth: 1200 }}>
          <Grid container spacing={4} justifyContent="center">
            <MetricCard
              title="Total Sales Revenue"
              value={metrics?.total_sales || 0}
              unit="$"
              subtitle="Across all products and time periods"
              icon={<SalesIcon sx={{ color: '#4CAF50', fontSize: 32 }} />}
              color="#4CAF50"
              trend="+12.5%"
              loading={loading}
            />
            
            <MetricCard
              title="Total Ad Investment"
              value={metrics?.total_ad_spend || 0}
              unit="$"
              subtitle="Investment in advertising campaigns"
              icon={<AdIcon sx={{ color: '#FF9800', fontSize: 32 }} />}
              color="#FF9800"
              trend="+8.3%"
              loading={loading}
            />
            
            <MetricCard
              title="ROAS Performance"
              value={metrics?.total_roas ? `${metrics.total_roas.toFixed(2)}x` : '0.00x'}
              subtitle="Return on advertising spend"
              icon={<RoasIcon sx={{ color: '#2196F3', fontSize: 32 }} />}
              color="#2196F3"
              trend="+15.7%"
              loading={loading}
            />
          </Grid>
        </Box>
      </Box>

      {/* Centered Ask AI Call-to-Action */}
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'center', 
        mb: 6
      }}>
        <Card sx={{
          background: 'linear-gradient(135deg, rgba(240, 147, 251, 0.15) 0%, rgba(245, 87, 108, 0.15) 100%)',
          border: '1px solid rgba(240, 147, 251, 0.3)',
          borderRadius: 4,
          maxWidth: 600,
          width: '100%',
          textAlign: 'center',
          p: 4,
          position: 'relative',
          overflow: 'hidden',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%)',
            transform: 'translateX(-100%)',
            animation: 'shimmer 3s infinite',
            '@keyframes shimmer': {
              '0%': { transform: 'translateX(-100%)' },
              '100%': { transform: 'translateX(100%)' }
            }
          }
        }}>
          <CardContent sx={{ position: 'relative', zIndex: 1 }}>
            <Box sx={{ mb: 3 }}>
              <SparkleIcon sx={{ 
                fontSize: 48, 
                color: '#f093fb',
                filter: 'drop-shadow(0 4px 8px rgba(240, 147, 251, 0.3))'
              }} />
            </Box>
            
            <Typography 
              variant="h4" 
              sx={{ 
                fontWeight: 700,
                mb: 2,
                background: 'linear-gradient(45deg, #f093fb, #f5576c)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              Ask AI Anything
            </Typography>
            
            <Typography 
              variant="h6" 
              sx={{ 
                color: 'rgba(255, 255, 255, 0.8)',
                mb: 3,
                lineHeight: 1.6
              }}
            >
              Get instant insights from your e-commerce data using natural language queries powered by Mistral AI
            </Typography>
            
            <Button
              variant="contained"
              size="large"
              startIcon={<AIIcon />}
              onClick={handleAskAI}
              sx={{
                background: 'linear-gradient(45deg, #f093fb, #f5576c)',
                color: 'white',
                px: 4,
                py: 2,
                borderRadius: '30px',
                fontWeight: 700,
                fontSize: '1.1rem',
                boxShadow: '0 8px 24px rgba(240, 147, 251, 0.4)',
                transition: 'all 0.3s ease',
                position: 'relative',
                overflow: 'hidden',
                '&:hover': {
                  background: 'linear-gradient(45deg, #ed7ef8, #f04462)',
                  transform: 'translateY(-3px) scale(1.05)',
                  boxShadow: '0 12px 32px rgba(240, 147, 251, 0.6)',
                },
                '&::before': {
                  content: '""',
                  position: 'absolute',
                  top: 0,
                  left: '-100%',
                  width: '100%',
                  height: '100%',
                  background: 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent)',
                  transition: 'left 0.5s ease',
                },
                '&:hover::before': {
                  left: '100%',
                }
              }}
            >
              Start Analyzing Your Data
            </Button>
            
            <Typography 
              variant="body2" 
              sx={{ 
                color: 'rgba(255, 255, 255, 0.6)',
                mt: 2,
                fontStyle: 'italic'
              }}
            >
              Try: "What is my total sales?" or "Calculate my ROAS"
            </Typography>
          </CardContent>
        </Card>
      </Box>

      <Divider sx={{ 
        mb: 6, 
        borderColor: 'rgba(255, 255, 255, 0.1)',
        '&::before, &::after': {
          borderColor: 'rgba(255, 255, 255, 0.1)'
        }
      }} />

      {/* Secondary Content */}
      <Grid container spacing={4}>
        {/* Data Processing Status */}
        <Grid item xs={12} lg={8}>
          <Paper sx={{ 
            p: 4, 
            background: 'rgba(255, 255, 255, 0.05)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: 3
          }}>
            <Typography variant="h5" sx={{ color: 'white', mb: 3, fontWeight: 600 }}>
              📊 Data Processing Status
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body1" sx={{ color: 'white', fontWeight: 500 }}>
                      Product Eligibility
                    </Typography>
                    <Typography variant="body2" sx={{ color: '#4CAF50' }}>
                      4,381 records
                    </Typography>
                  </Box>
                  <LinearProgress 
                    variant="determinate" 
                    value={100} 
                    sx={{ 
                      height: 8, 
                      borderRadius: 4,
                      backgroundColor: 'rgba(76, 175, 80, 0.2)',
                      '& .MuiLinearProgress-bar': {
                        background: 'linear-gradient(45deg, #4CAF50, #66BB6A)',
                        borderRadius: 4
                      }
                    }} 
                  />
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body1" sx={{ color: 'white', fontWeight: 500 }}>
                      Ad Sales Data
                    </Typography>
                    <Typography variant="body2" sx={{ color: '#FF9800' }}>
                      3,696 records
                    </Typography>
                  </Box>
                  <LinearProgress 
                    variant="determinate" 
                    value={100} 
                    sx={{ 
                      height: 8, 
                      borderRadius: 4,
                      backgroundColor: 'rgba(255, 152, 0, 0.2)',
                      '& .MuiLinearProgress-bar': {
                        background: 'linear-gradient(45deg, #FF9800, #FFB74D)',
                        borderRadius: 4
                      }
                    }} 
                  />
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body1" sx={{ color: 'white', fontWeight: 500 }}>
                      Total Sales
                    </Typography>
                    <Typography variant="body2" sx={{ color: '#2196F3' }}>
                      702 records
                    </Typography>
                  </Box>
                  <LinearProgress 
                    variant="determinate" 
                    value={100} 
                    sx={{ 
                      height: 8, 
                      borderRadius: 4,
                      backgroundColor: 'rgba(33, 150, 243, 0.2)',
                      '& .MuiLinearProgress-bar': {
                        background: 'linear-gradient(45deg, #2196F3, #64B5F6)',
                        borderRadius: 4
                      }
                    }} 
                  />
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} lg={4}>
          <Typography variant="h6" sx={{ color: 'white', mb: 3, fontWeight: 600 }}>
            🚀 Quick Actions
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={6} lg={12}>
              <QuickActionCard
                title="View Analytics"
                description="Deep dive into your data"
                icon={<AssessmentIcon />}
                color="#667eea"
                onClick={() => handleAskAI()}
              />
            </Grid>
            <Grid item xs={6} lg={12}>
              <QuickActionCard
                title="Export Data"
                description="Download reports"
                icon={<DownloadIcon />}
                color="#f093fb"
                onClick={() => {/* Export functionality */}}
              />
            </Grid>
          </Grid>
        </Grid>
      </Grid>

      {/* Floating Action Button for Mobile */}
      <Fab
        color="primary"
        sx={{
          position: 'fixed',
          bottom: 24,
          right: 24,
          background: 'linear-gradient(45deg, #f093fb, #f5576c)',
          '&:hover': {
            background: 'linear-gradient(45deg, #ed7ef8, #f04462)',
          },
          display: { xs: 'flex', sm: 'none' }, // Only show on mobile
          zIndex: 1000
        }}
        onClick={handleAskAI}
      >
        <AIIcon />
      </Fab>
    </Box>
  );
};

export default Dashboard;
