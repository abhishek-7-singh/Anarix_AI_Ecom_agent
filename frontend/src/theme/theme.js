// src/theme/theme.js
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#667eea',
      light: '#8b9cee',
      dark: '#4c63d2',
    },
    secondary: {
      main: '#f093fb',
      light: '#f3a8fc',
      dark: '#ed7ef8',
    },
    background: {
      default: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
      paper: 'rgba(255, 255, 255, 0.1)',
    },
    text: {
      primary: '#ffffff',
      secondary: 'rgba(255, 255, 255, 0.7)',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '3rem',
      fontWeight: 700,
      background: 'linear-gradient(45deg, #667eea, #764ba2)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
    },
    h2: {
      fontSize: '2.5rem',
      fontWeight: 600,
      color: '#ffffff',
    },
    h4: {
      fontSize: '2rem',
      fontWeight: 600,
      background: 'linear-gradient(45deg, #f093fb, #f5576c)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          background: 'rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          borderRadius: '20px',
          boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '15px',
          textTransform: 'none',
          fontWeight: 600,
          padding: '12px 24px',
        },
        contained: {
          background: 'linear-gradient(45deg, #667eea, #764ba2)',
          boxShadow: '0 4px 15px 0 rgba(102, 126, 234, 0.4)',
          '&:hover': {
            background: 'linear-gradient(45deg, #5a67d8, #6b46c1)',
            boxShadow: '0 6px 20px 0 rgba(102, 126, 234, 0.6)',
          },
        },
      },
    },
  },
});
