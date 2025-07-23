// import React, { useState, Suspense } from 'react';
// import {
//   Box,
//   Card,
//   CardContent,
//   Typography,
//   Button,
//   ButtonGroup,
//   Grid,
//   Paper,
//   CircularProgress,
//   Alert
// } from '@mui/material';
// import {
//   ArrowBack as BackIcon,
//   BarChart as BarIcon,
//   PieChart as PieIcon,
//   ShowChart as LineIcon,
//   ThreeDRotation as ThreeDIcon
// } from '@mui/icons-material';

// // Lazy load 3D components
// const Chart3D = React.lazy(() => import('./Chart3D'));
// const BarChart3D = React.lazy(() => import('./BarChart3D'));
// const PieChart3D = React.lazy(() => import('./PieChart3D'));
// const LineChart3D = React.lazy(() => import('./LineChart3D'));

// const ChartViewer = ({ data, onBack }) => {
//   const [chartType, setChartType] = useState(data?.chart_data?.type || 'bar');
//   const [is3D, setIs3D] = useState(true);

//   if (!data?.chart_data) {
//     return (
//       <Card elevation={3}>
//         <CardContent>
//           <Alert severity="warning">
//             No chart data available for this query.
//           </Alert>
//           <Button
//             startIcon={<BackIcon />}
//             onClick={onBack}
//             sx={{ mt: 2 }}
//           >
//             Back to Query
//           </Button>
//         </CardContent>
//       </Card>
//     );
//   }

//   const { chart_data } = data;
//   const processedData = chart_data.data?.map((item, index) => ({
//     id: index,
//     label: item.label || `Item ${index}`,
//     value: parseFloat(item.value || item.y || 0),
//     color: item.color || `hsl(${index * 40}, 70%, 50%)`,
//     ...item
//   })) || [];

//   const renderChart = () => {
//     if (processedData.length === 0) {
//       return (
//         <Alert severity="info">
//           No data available to display in chart.
//         </Alert>
//       );
//     }

//     const commonProps = {
//       data: processedData,
//       title: chart_data.title,
//       config: chart_data.config
//     };

//     if (is3D) {
//       return (
//         <Suspense fallback={<CircularProgress />}>
//           {chartType === 'bar' && <BarChart3D {...commonProps} />}
//           {chartType === 'pie' && <PieChart3D {...commonProps} />}
//           {chartType === 'line' && <LineChart3D {...commonProps} />}
//         </Suspense>
//       );
//     }

//     // 2D fallback charts would go here
//     return <div>2D charts not implemented yet</div>;
//   };

//   return (
//     <Box sx={{ maxWidth: 1400, mx: 'auto' }}>
//       <Card elevation={3} sx={{ mb: 3 }}>
//         <CardContent>
//           <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
//             <Typography variant="h5" color="primary">
//               {chart_data.title}
//             </Typography>
//             <Button
//               startIcon={<BackIcon />}
//               onClick={onBack}
//               variant="outlined"
//             >
//               Back to Query
//             </Button>
//           </Box>

//           <Grid container spacing={2} alignItems="center">
//             <Grid item xs={12} md={6}>
//               <Typography variant="subtitle2" gutterBottom>
//                 Chart Type
//               </Typography>
//               <ButtonGroup variant="outlined" size="small">
//                 <Button
//                   startIcon={<BarIcon />}
//                   variant={chartType === 'bar' ? 'contained' : 'outlined'}
//                   onClick={() => setChartType('bar')}
//                 >
//                   Bar
//                 </Button>
//                 <Button
//                   startIcon={<PieIcon />}
//                   variant={chartType === 'pie' ? 'contained' : 'outlined'}
//                   onClick={() => setChartType('pie')}
//                 >
//                   Pie
//                 </Button>
//                 <Button
//                   startIcon={<LineIcon />}
//                   variant={chartType === 'line' ? 'contained' : 'outlined'}
//                   onClick={() => setChartType('line')}
//                 >
//                   Line
//                 </Button>
//               </ButtonGroup>
//             </Grid>

//             <Grid item xs={12} md={6}>
//               <Typography variant="subtitle2" gutterBottom>
//                 Visualization Mode
//               </Typography>
//               <Button
//                 startIcon={<ThreeDIcon />}
//                 variant={is3D ? 'contained' : 'outlined'}
//                 onClick={() => setIs3D(!is3D)}
//                 color={is3D ? 'primary' : 'inherit'}
//               >
//                 3D Mode
//               </Button>
//             </Grid>
//           </Grid>
//         </CardContent>
//       </Card>

//       <Card elevation={3}>
//         <CardContent>
//           <Box sx={{ height: '600px', position: 'relative' }}>
//             {renderChart()}
//           </Box>
//         </CardContent>
//       </Card>

//       <Card elevation={2} sx={{ mt: 3 }}>
//         <CardContent>
//           <Typography variant="h6" gutterBottom>
//             Chart Information
//           </Typography>
//           <Grid container spacing={2}>
//             <Grid item xs={12} md={6}>
//               <Paper variant="outlined" sx={{ p: 2 }}>
//                 <Typography variant="subtitle2" color="textSecondary" gutterBottom>
//                   Data Points
//                 </Typography>
//                 <Typography variant="h6">
//                   {processedData.length}
//                 </Typography>
//               </Paper>
//             </Grid>
//             <Grid item xs={12} md={6}>
//               <Paper variant="outlined" sx={{ p: 2 }}>
//                 <Typography variant="subtitle2" color="textSecondary" gutterBottom>
//                   Total Value
//                 </Typography>
//                 <Typography variant="h6">
//                   {processedData.reduce((sum, item) => sum + item.value, 0).toLocaleString()}
//                 </Typography>
//               </Paper>
//             </Grid>
//           </Grid>

//           <Typography variant="subtitle2" sx={{ mt: 2, mb: 1 }}>
//             Controls (3D Mode)
//           </Typography>
//           <Box component="ul" sx={{ m: 0, pl: 2 }}>
//             <li>Left click + drag: Rotate view</li>
//             <li>Right click + drag: Pan view</li>
//             <li>Scroll wheel: Zoom in/out</li>
//             <li>Double-click: Reset view</li>
//           </Box>
//         </CardContent>
//       </Card>
//     </Box>
//   );
// };

// export default ChartViewer;
import React, { useState, Suspense } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  ButtonGroup,
  Grid,
  Paper,
  CircularProgress,
  Alert,
  Divider
} from '@mui/material';
import {
  ArrowBack as BackIcon,
  BarChart as BarIcon,
  PieChart as PieIcon,
  ShowChart as LineIcon,
  ThreeDRotation as ThreeDIcon
} from '@mui/icons-material';

// Lazy load 3D components
const Chart3D = React.lazy(() => import('./Chart3D'));
const BarChart3D = React.lazy(() => import('./BarChart3D'));
const PieChart3D = React.lazy(() => import('./PieChart3D'));
const LineChart3D = React.lazy(() => import('./LineChart3D'));

const ChartViewer = ({ data, onBack }) => {
  const [chartType, setChartType] = useState(data?.chart_data?.type || 'bar');
  const [is3D, setIs3D] = useState(true);

  if (!data?.chart_data) {
    return (
      <Card elevation={3}>
        <CardContent>
          <Alert severity="warning">
            No chart data available for this query.
          </Alert>
          <Button
            startIcon={<BackIcon />}
            onClick={onBack}
            sx={{ mt: 2 }}
          >
            Back to Query
          </Button>
        </CardContent>
      </Card>
    );
  }

  const { chart_data } = data;
  const processedData = chart_data.data?.map((item, index) => ({
    id: index,
    label: item.label || `Item ${index}`,
    value: parseFloat(item.value || item.y || 0),
    color: item.color || `hsl(${index * 40}, 70%, 50%)`,
    // Add item name/details if available
    itemName: item.item_name || item.product_name || item.label,
    itemId: item.item_id || item.id,
    ...item
  })) || [];

  // Get the top items for display
  const getTopItems = () => {
    const sortedData = [...processedData].sort((a, b) => b.value - a.value);
    return sortedData.slice(0, 5); // Show top 5
  };

  const renderChart = () => {
    if (processedData.length === 0) {
      return (
        <Alert severity="info">
          No data available to display in chart.
        </Alert>
      );
    }

    const commonProps = {
      data: processedData,
      title: chart_data.title,
      config: chart_data.config
    };

    if (is3D) {
      return (
        <Suspense fallback={<CircularProgress />}>
          {chartType === 'bar' && <BarChart3D {...commonProps} />}
          {chartType === 'pie' && <PieChart3D {...commonProps} />}
          {chartType === 'line' && <LineChart3D {...commonProps} />}
        </Suspense>
      );
    }

    return <div>2D charts not implemented yet</div>;
  };

  return (
    <Box sx={{ maxWidth: 1400, mx: 'auto' }}>
      {/* AI Response Section - NEW */}
      {data.response && (
        <Card elevation={3} sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom color="primary">
              AI Analysis
            </Typography>
            <Paper 
              variant="outlined" 
              sx={{ 
                p: 3, 
                bgcolor: 'background.default',
                borderLeft: '4px solid',
                borderLeftColor: 'primary.main'
              }}
            >
              <Typography 
                variant="body1" 
                sx={{ 
                  whiteSpace: 'pre-wrap',
                  lineHeight: 1.6,
                  fontSize: '1.1rem'
                }}
              >
                {data.response}
              </Typography>
            </Paper>

            {/* Top Items Summary - NEW */}
            {processedData.length > 0 && (
              <Box sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Key Items in this Analysis
                </Typography>
                <Grid container spacing={2}>
                  {getTopItems().map((item, index) => (
                    <Grid item xs={12} sm={6} md={4} key={index}>
                      <Paper 
                        variant="outlined" 
                        sx={{ 
                          p: 2,
                          textAlign: 'center',
                          bgcolor: index === 0 ? 'primary.light' : 'background.paper',
                          color: index === 0 ? 'primary.contrastText' : 'text.primary'
                        }}
                      >
                        <Typography variant="h6" component="div">
                          {item.itemName || `Product ${item.itemId || item.id}`}
                        </Typography>
                        <Typography variant="h4" sx={{ fontWeight: 'bold', my: 1 }}>
                          {typeof item.value === 'number' 
                            ? item.value.toLocaleString() 
                            : item.value}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          {index === 0 ? '🏆 Top Performer' : `#${index + 1}`}
                        </Typography>
                      </Paper>
                    </Grid>
                  ))}
                </Grid>
              </Box>
            )}
            
            <Divider sx={{ my: 3 }} />
          </CardContent>
        </Card>
      )}

      {/* Chart Controls */}
      <Card elevation={3} sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h5" color="primary">
              {chart_data.title}
            </Typography>
            <Button
              startIcon={<BackIcon />}
              onClick={onBack}
              variant="outlined"
            >
              Back to Query
            </Button>
          </Box>

          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                Chart Type
              </Typography>
              <ButtonGroup variant="outlined" size="small">
                <Button
                  startIcon={<BarIcon />}
                  variant={chartType === 'bar' ? 'contained' : 'outlined'}
                  onClick={() => setChartType('bar')}
                >
                  Bar
                </Button>
                <Button
                  startIcon={<PieIcon />}
                  variant={chartType === 'pie' ? 'contained' : 'outlined'}
                  onClick={() => setChartType('pie')}
                >
                  Pie
                </Button>
                <Button
                  startIcon={<LineIcon />}
                  variant={chartType === 'line' ? 'contained' : 'outlined'}
                  onClick={() => setChartType('line')}
                >
                  Line
                </Button>
              </ButtonGroup>
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                Visualization Mode
              </Typography>
              <Button
                startIcon={<ThreeDIcon />}
                variant={is3D ? 'contained' : 'outlined'}
                onClick={() => setIs3D(!is3D)}
                color={is3D ? 'primary' : 'inherit'}
              >
                3D Mode
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* 3D Chart Display */}
      <Card elevation={3}>
        <CardContent>
          <Box sx={{ height: '600px', position: 'relative' }}>
            {renderChart()}
          </Box>
        </CardContent>
      </Card>

      {/* Chart Information */}
      <Card elevation={2} sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Chart Information
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Paper variant="outlined" sx={{ p: 2 }}>
                <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                  Data Points
                </Typography>
                <Typography variant="h6">
                  {processedData.length}
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper variant="outlined" sx={{ p: 2 }}>
                <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                  Total Value
                </Typography>
                <Typography variant="h6">
                  {processedData.reduce((sum, item) => sum + item.value, 0).toLocaleString()}
                </Typography>
              </Paper>
            </Grid>
          </Grid>

          <Typography variant="subtitle2" sx={{ mt: 2, mb: 1 }}>
            Controls (3D Mode)
          </Typography>
          <Box component="ul" sx={{ m: 0, pl: 2 }}>
            <li>Left click + drag: Rotate view</li>
            <li>Right click + drag: Pan view</li>
            <li>Scroll wheel: Zoom in/out</li>
            <li>Double-click: Reset view</li>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ChartViewer;
