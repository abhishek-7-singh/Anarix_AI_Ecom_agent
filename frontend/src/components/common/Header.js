import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';

const Header = ({ currentView, setCurrentView, healthStatus }) => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          E-commerce AI Agent
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button 
            color="inherit" 
            variant={currentView === 'dashboard' ? 'outlined' : 'text'}
            onClick={() => setCurrentView('dashboard')}
          >
            Dashboard
          </Button>
          <Button 
            color="inherit" 
            variant={currentView === 'query' ? 'outlined' : 'text'}
            onClick={() => setCurrentView('query')}
          >
            Ask AI
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
