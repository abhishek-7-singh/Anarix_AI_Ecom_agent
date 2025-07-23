import React, { useState, useEffect } from 'react';
import { Typography, Box } from '@mui/material';

const StreamingText = ({ 
  text, 
  speed = 50, 
  onComplete,
  startDelay = 0,
  showCursor = true 
}) => {
  const [displayedText, setDisplayedText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isComplete, setIsComplete] = useState(false);
  const [showBlinkingCursor, setShowBlinkingCursor] = useState(true);

  useEffect(() => {
    if (!text) return;

    const timeout = setTimeout(() => {
      if (currentIndex < text.length) {
        setDisplayedText(text.slice(0, currentIndex + 1));
        setCurrentIndex(currentIndex + 1);
      } else if (!isComplete) {
        setIsComplete(true);
        if (onComplete) {
          onComplete();
        }
      }
    }, currentIndex === 0 ? startDelay : speed);

    return () => clearTimeout(timeout);
  }, [text, currentIndex, speed, startDelay, isComplete, onComplete]);

  // Cursor blinking effect
  useEffect(() => {
    if (!showCursor || !isComplete) return;

    const interval = setInterval(() => {
      setShowBlinkingCursor(prev => !prev);
    }, 500);

    return () => clearInterval(interval);
  }, [showCursor, isComplete]);

  // Reset when text changes
  useEffect(() => {
    setDisplayedText('');
    setCurrentIndex(0);
    setIsComplete(false);
    setShowBlinkingCursor(true);
  }, [text]);

  return (
    <Box>
      <Typography 
        variant="body1" 
        component="div"
        sx={{ 
          whiteSpace: 'pre-wrap',
          minHeight: '1.5em',
          fontFamily: 'inherit',
        }}
      >
        {displayedText}
        {showCursor && (showBlinkingCursor || !isComplete) && (
          <Box
            component="span"
            sx={{
              borderRight: '2px solid currentColor',
              animation: isComplete ? 'blink 1s infinite' : 'none',
              '@keyframes blink': {
                '0%, 50%': { 
                  borderColor: 'currentColor',
                },
                '51%, 100%': { 
                  borderColor: 'transparent',
                }
              }
            }}
          />
        )}
      </Typography>
    </Box>
  );
};

export default StreamingText;
