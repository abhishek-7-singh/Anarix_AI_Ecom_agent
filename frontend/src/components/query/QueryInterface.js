// import React, { useState, useRef, useEffect } from 'react';
// import {
//   Box,
//   Card,
//   CardContent,
//   TextField,
//   Button,
//   Typography,
//   Chip,
//   Grid,
//   Paper,
//   IconButton,
//   Switch,
//   FormControlLabel,
//   CircularProgress,
//   Fade,
//   Alert
// } from '@mui/material';
// import {
//   Send as SendIcon,
//   Clear as ClearIcon,
//   ContentCopy as CopyIcon,
//   Visibility as ViewIcon
// } from '@mui/icons-material';

// import StreamingText from './StreamingText';
// import { useQuery } from '../../contexts/QueryContext';
// import { apiClient } from '../../services/api';

// const QueryInterface = ({ onResult, onError }) => {
//   const [question, setQuestion] = useState('');
//   const [loading, setLoading] = useState(false);
//   const [result, setResult] = useState(null);
//   const [streamMode, setStreamMode] = useState(true);
//   const [examples, setExamples] = useState([]);
//   const textFieldRef = useRef();

//   const { addQuery, queryHistory } = useQuery();

//   useEffect(() => {
//     loadExamples();
//   }, []);

//   const loadExamples = async () => {
//     try {
//       // ✅ FIXED: Added /api prefix
//       const response = await apiClient.get('/api/query/examples');
//       setExamples(response.data.examples);
//     } catch (err) {
//       console.error('Failed to load examples:', err);
//     }
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!question.trim() || loading) return;

//     setLoading(true);
//     setResult(null);

//     try {
//       // ✅ FIXED: Added /api prefix
//       const response = await apiClient.post('/api/query', {
//         question: question.trim(),
//         stream: streamMode,
//         include_chart: true
//       });

//       const queryResult = response.data;
//       setResult(queryResult);
      
//       // Add to history
//       addQuery({
//         question: question.trim(),
//         result: queryResult,
//         timestamp: new Date().toISOString()
//       });

//       // Notify parent component
//       if (onResult) {
//         onResult(queryResult);
//       }

//     } catch (err) {
//       const errorMessage = err.response?.data?.detail || 'Query failed. Please try again.';
//       onError(errorMessage);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const handleExampleClick = (example) => {
//     setQuestion(example);
//     textFieldRef.current?.focus();
//   };

//   const handleClearQuery = () => {
//     setQuestion('');
//     setResult(null);
//     textFieldRef.current?.focus();
//   };

//   const handleCopySQL = () => {
//     if (result?.sql_query) {
//       navigator.clipboard.writeText(result.sql_query);
//     }
//   };

//   const handleViewChart = () => {
//     if (result && onResult) {
//       onResult(result);
//     }
//   };

//   return (
//     <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
//       <Typography variant="h4" gutterBottom align="center" color="primary">
//         Ask Your E-commerce Data Anything
//       </Typography>
      
//       <Card elevation={3} sx={{ mb: 4 }}>
//         <CardContent>
//           <form onSubmit={handleSubmit}>
//             <TextField
//               ref={textFieldRef}
//               fullWidth
//               multiline
//               rows={3}
//               value={question}
//               onChange={(e) => setQuestion(e.target.value)}
//               placeholder="Ask a question about your e-commerce data..."
//               variant="outlined"
//               sx={{ mb: 2 }}
//               disabled={loading}
//             />
            
//             <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
//               <FormControlLabel
//                 control={
//                   <Switch
//                     checked={streamMode}
//                     onChange={(e) => setStreamMode(e.target.checked)}
//                     disabled={loading}
//                   />
//                 }
//                 label="Stream Response (typing effect)"
//               />
              
//               <Box>
//                 <IconButton onClick={handleClearQuery} disabled={loading}>
//                   <ClearIcon />
//                 </IconButton>
//                 <Button
//                   type="submit"
//                   variant="contained"
//                   startIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
//                   disabled={loading || !question.trim()}
//                   sx={{ ml: 1 }}
//                 >
//                   {loading ? 'Analyzing...' : 'Ask AI'}
//                 </Button>
//               </Box>
//             </Box>
//           </form>
//         </CardContent>
//       </Card>

//       {/* Example Questions */}
//       <Card elevation={2} sx={{ mb: 4 }}>
//         <CardContent>
//           <Typography variant="h6" gutterBottom>
//             Example Questions
//           </Typography>
//           <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
//             {examples.map((example, index) => (
//               <Chip
//                 key={index}
//                 label={example}
//                 onClick={() => handleExampleClick(example)}
//                 variant="outlined"
//                 clickable
//                 disabled={loading}
//                 sx={{ mb: 1 }}
//               />
//             ))}
//           </Box>
//         </CardContent>
//       </Card>

//       {/* Query Result */}
//       {result && (
//         <Fade in={!!result}>
//           <Card elevation={3}>
//             <CardContent>
//               <Typography variant="h6" gutterBottom>
//                 AI Response
//               </Typography>
              
//               <Paper variant="outlined" sx={{ p: 2, mb: 2, bgcolor: 'background.default' }}>
//                 {streamMode ? (
//                   <StreamingText text={result.response} />
//                 ) : (
//                   <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
//                     {result.response}
//                   </Typography>
//                 )}
//               </Paper>

//               {result.sql_query && (
//                 <Box sx={{ mb: 2 }}>
//                   <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
//                     <Typography variant="subtitle1" color="textSecondary">
//                       Generated SQL Query
//                     </Typography>
//                     <IconButton size="small" onClick={handleCopySQL} sx={{ ml: 1 }}>
//                       <CopyIcon fontSize="small" />
//                     </IconButton>
//                   </Box>
//                   <Paper variant="outlined" sx={{ p: 2, bgcolor: '#f5f5f5' }}>
//                     <Typography
//                       variant="body2"
//                       component="pre"
//                       sx={{ fontFamily: 'monospace', fontSize: '0.875rem', whiteSpace: 'pre-wrap' }}
//                     >
//                       {result.sql_query}
//                     </Typography>
//                   </Paper>
//                 </Box>
//               )}

//               {result.results && (
//                 <Alert severity="info" sx={{ mb: 2 }}>
//                   Found {result.results.length} result{result.results.length !== 1 ? 's' : ''}
//                   {result.execution_time && ` in ${result.execution_time.toFixed(2)}s`}
//                 </Alert>
//               )}

//               {result.chart_data && (
//                 <Button
//                   variant="outlined"
//                   startIcon={<ViewIcon />}
//                   onClick={handleViewChart}
//                   sx={{ mt: 1 }}
//                 >
//                   View Interactive Chart
//                 </Button>
//               )}
//             </CardContent>
//           </Card>
//         </Fade>
//       )}

//       {/* Query History */}
//       {queryHistory.length > 0 && (
//         <Card elevation={2} sx={{ mt: 4 }}>
//           <CardContent>
//             <Typography variant="h6" gutterBottom>
//             Recent Queries
//             </Typography>
//             {queryHistory.slice(-5).reverse().map((query, index) => (
//               <Paper
//                 key={index}
//                 variant="outlined"
//                 sx={{ p: 2, mb: 1, cursor: 'pointer' }}
//                 onClick={() => handleExampleClick(query.question)}
//               >
//                 <Typography variant="body2" color="textSecondary">
//                   {new Date(query.timestamp).toLocaleString()}
//                 </Typography>
//                 <Typography variant="body1">
//                   {query.question}
//                 </Typography>
//               </Paper>
//             ))}
//           </CardContent>
//         </Card>
//       )}
//     </Box>
//   );
// };

// export default QueryInterface;
import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Chip,
  Grid,
  Paper,
  IconButton,
  Switch,
  FormControlLabel,
  CircularProgress,
  Fade,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import {
  Send as SendIcon,
  Clear as ClearIcon,
  ContentCopy as CopyIcon,
  Visibility as ViewIcon,
  ExpandMore as ExpandMoreIcon
} from '@mui/icons-material';

import StreamingText from './StreamingText';
import { useQuery } from '../../contexts/QueryContext';
import { apiClient } from '../../services/api';

const QueryInterface = ({ onResult, onError }) => {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [streamMode, setStreamMode] = useState(true);
  const [examples, setExamples] = useState({});  // Changed to object
  const [allExamples, setAllExamples] = useState([]);  // Flattened array for compatibility
  const textFieldRef = useRef();

  const { addQuery, queryHistory } = useQuery();

  useEffect(() => {
    loadExamples();
  }, []);

  const loadExamples = async () => {
    try {
      const response = await apiClient.get('/api/query/examples');
      const examplesData = response.data.examples;
      
      // Handle both old and new format
      if (Array.isArray(examplesData)) {
        // Old format - simple array
        setExamples({ general: examplesData });
        setAllExamples(examplesData);
      } else if (typeof examplesData === 'object') {
        // New format - categorized object
        setExamples(examplesData);
        
        // Flatten all examples into a single array for backward compatibility
        const flattened = Object.values(examplesData).flat();
        setAllExamples(flattened);
      } else {
        // Fallback
        setExamples({});
        setAllExamples([]);
      }
    } catch (err) {
      console.error('Failed to load examples:', err);
      // Set fallback examples
      setExamples({
        basic: [
          "What is my total sales?",
          "Calculate the Return on Ad Spend (ROAS)",
          "Which product had the highest CPC (Cost Per Click)?"
        ]
      });
      setAllExamples([
        "What is my total sales?",
        "Calculate the Return on Ad Spend (ROAS)",
        "Which product had the highest CPC (Cost Per Click)?"
      ]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await apiClient.post('/api/query', {
        question: question.trim(),
        stream: streamMode,
        include_chart: true
      });

      const queryResult = response.data;
      setResult(queryResult);
      
      // Add to history
      addQuery({
        question: question.trim(),
        result: queryResult,
        timestamp: new Date().toISOString()
      });

      // Notify parent component
      if (onResult) {
        onResult(queryResult);
      }

    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Query failed. Please try again.';
      onError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (example) => {
    setQuestion(example);
    textFieldRef.current?.focus();
  };

  const handleClearQuery = () => {
    setQuestion('');
    setResult(null);
    textFieldRef.current?.focus();
  };

  const handleCopySQL = () => {
    if (result?.sql_query) {
      navigator.clipboard.writeText(result.sql_query);
    }
  };

  const handleViewChart = () => {
    if (result && onResult) {
      onResult(result);
    }
  };

  // Format category name for display
  const formatCategoryName = (category) => {
    return category
      .replace(/_/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h4" gutterBottom align="center" color="primary">
        Ask Your E-commerce Data Anything
      </Typography>
      
      <Card elevation={3} sx={{ mb: 4 }}>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <TextField
              ref={textFieldRef}
              fullWidth
              multiline
              rows={3}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question about your e-commerce data..."
              variant="outlined"
              sx={{ mb: 2 }}
              disabled={loading}
            />
            
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={streamMode}
                    onChange={(e) => setStreamMode(e.target.checked)}
                    disabled={loading}
                  />
                }
                label="Stream Response (typing effect)"
              />
              
              <Box>
                <IconButton onClick={handleClearQuery} disabled={loading}>
                  <ClearIcon />
                </IconButton>
                <Button
                  type="submit"
                  variant="contained"
                  startIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
                  disabled={loading || !question.trim()}
                  sx={{ ml: 1 }}
                >
                  {loading ? 'Analyzing...' : 'Ask AI'}
                </Button>
              </Box>
            </Box>
          </form>
        </CardContent>
      </Card>

      {/* Enhanced Example Questions with Categories */}
      <Card elevation={2} sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Example Questions
          </Typography>
          
          {Object.keys(examples).length > 1 ? (
            // Show categorized examples
            <Box>
              {Object.entries(examples).map(([category, categoryExamples]) => (
                <Accordion key={category} sx={{ mb: 1 }}>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                      {formatCategoryName(category)} ({categoryExamples.length})
                    </Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                      {categoryExamples.map((example, index) => (
                        <Chip
                          key={`${category}-${index}`}
                          label={example}
                          onClick={() => handleExampleClick(example)}
                          variant="outlined"
                          clickable
                          disabled={loading}
                          sx={{ mb: 1 }}
                        />
                      ))}
                    </Box>
                  </AccordionDetails>
                </Accordion>
              ))}
            </Box>
          ) : (
            // Fallback to simple list
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {allExamples.map((example, index) => (
                <Chip
                  key={index}
                  label={example}
                  onClick={() => handleExampleClick(example)}
                  variant="outlined"
                  clickable
                  disabled={loading}
                  sx={{ mb: 1 }}
                />
              ))}
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Query Result */}
      {result && (
        <Fade in={!!result}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                AI Response
              </Typography>
              
              <Paper variant="outlined" sx={{ p: 2, mb: 2, bgcolor: 'background.default' }}>
                {streamMode ? (
                  <StreamingText text={result.response} />
                ) : (
                  <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                    {result.response}
                  </Typography>
                )}
              </Paper>

              {result.sql_query && (
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Typography variant="subtitle1" color="textSecondary">
                      Generated SQL Query
                    </Typography>
                    <IconButton size="small" onClick={handleCopySQL} sx={{ ml: 1 }}>
                      <CopyIcon fontSize="small" />
                    </IconButton>
                  </Box>
                  <Paper variant="outlined" sx={{ p: 2, bgcolor: '#f5f5f5' }}>
                    <Typography
                      variant="body2"
                      component="pre"
                      sx={{ fontFamily: 'monospace', fontSize: '0.875rem', whiteSpace: 'pre-wrap' }}
                    >
                      {result.sql_query}
                    </Typography>
                  </Paper>
                </Box>
              )}

              {result.results && (
                <Alert severity="info" sx={{ mb: 2 }}>
                  Found {result.results.length} result{result.results.length !== 1 ? 's' : ''}
                  {result.execution_time && ` in ${result.execution_time.toFixed(2)}s`}
                </Alert>
              )}

              {result.chart_data && (
                <Button
                  variant="outlined"
                  startIcon={<ViewIcon />}
                  onClick={handleViewChart}
                  sx={{ mt: 1 }}
                >
                  View Interactive Chart
                </Button>
              )}
            </CardContent>
          </Card>
        </Fade>
      )}

      {/* Query History */}
      {queryHistory.length > 0 && (
        <Card elevation={2} sx={{ mt: 4 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Recent Queries
            </Typography>
            {queryHistory.slice(-5).reverse().map((query, index) => (
              <Paper
                key={index}
                variant="outlined"
                sx={{ p: 2, mb: 1, cursor: 'pointer' }}
                onClick={() => handleExampleClick(query.question)}
              >
                <Typography variant="body2" color="textSecondary">
                  {new Date(query.timestamp).toLocaleString()}
                </Typography>
                <Typography variant="body1">
                  {query.question}
                </Typography>
              </Paper>
            ))}
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default QueryInterface;
