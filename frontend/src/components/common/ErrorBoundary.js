import React from 'react';
import { Alert, AlertTitle, Box, Button } from '@mui/material';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
  }

  handleReload = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <Box sx={{ p: 3, maxWidth: 600, mx: 'auto', mt: 4 }}>
          <Alert severity="error">
            <AlertTitle>Something went wrong</AlertTitle>
            <p>The application encountered an unexpected error.</p>
            
            {this.state.error && (
              <details style={{ whiteSpace: 'pre-wrap', marginTop: '1rem' }}>
                <summary>Error details</summary>
                <pre>{this.state.error && this.state.error.toString()}</pre>
                <pre>{this.state.errorInfo.componentStack}</pre>
              </details>
            )}
            
            <Button 
              variant="contained" 
              onClick={this.handleReload}
              sx={{ mt: 2 }}
            >
              Reload Application
            </Button>
          </Alert>
        </Box>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
