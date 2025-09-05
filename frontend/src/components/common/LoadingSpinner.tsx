import React from 'react';
import { Box, CircularProgress, Typography, Fade } from '@mui/material';
import { keyframes } from '@mui/system';

// Animación de pulse
const pulse = keyframes`
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
`;

// Animación de bounce
const bounce = keyframes`
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0,0,0);
  }
  40%, 43% {
    transform: translate3d(0, -8px, 0);
  }
  70% {
    transform: translate3d(0, -4px, 0);
  }
  90% {
    transform: translate3d(0, -2px, 0);
  }
`;

// Animación de dots
const dotAnimation = keyframes`
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
`;

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  message?: string;
  variant?: 'circular' | 'dots' | 'pulse';
  color?: 'primary' | 'secondary';
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'medium',
  message = 'Cargando...',
  variant = 'circular',
  color = 'primary'
}) => {
  const sizeMap = {
    small: 24,
    medium: 40,
    large: 60
  };

  if (variant === 'dots') {
    return (
      <Fade in={true}>
        <Box 
          display="flex" 
          flexDirection="column" 
          alignItems="center" 
          justifyContent="center"
          sx={{ py: 4 }}
        >
          <Box display="flex" gap={1} mb={2}>
            {[0, 1, 2].map((index) => (
              <Box
                key={index}
                sx={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  backgroundColor: color === 'primary' ? 'primary.main' : 'secondary.main',
                  animation: `${dotAnimation} 1.4s infinite ease-in-out`,
                  animationDelay: `${index * 0.16}s`,
                }}
              />
            ))}
          </Box>
          {message && (
            <Typography variant="body2" color="text.secondary">
              {message}
            </Typography>
          )}
        </Box>
      </Fade>
    );
  }

  if (variant === 'pulse') {
    return (
      <Fade in={true}>
        <Box 
          display="flex" 
          flexDirection="column" 
          alignItems="center" 
          justifyContent="center"
          sx={{ py: 4 }}
        >
          <Box
            sx={{
              width: sizeMap[size],
              height: sizeMap[size],
              borderRadius: '50%',
              backgroundColor: color === 'primary' ? 'primary.main' : 'secondary.main',
              animation: `${pulse} 1.5s infinite`,
              mb: 2,
            }}
          />
          {message && (
            <Typography variant="body2" color="text.secondary">
              {message}
            </Typography>
          )}
        </Box>
      </Fade>
    );
  }

  return (
    <Fade in={true}>
      <Box 
        display="flex" 
        flexDirection="column" 
        alignItems="center" 
        justifyContent="center"
        sx={{ py: 4 }}
      >
        <CircularProgress 
          size={sizeMap[size]} 
          color={color}
          sx={{
            mb: 2,
            animation: `${bounce} 2s infinite`,
          }}
        />
        {message && (
          <Typography variant="body2" color="text.secondary">
            {message}
          </Typography>
        )}
      </Box>
    </Fade>
  );
};

// Loading overlay para toda la página
interface LoadingOverlayProps {
  open: boolean;
  message?: string;
}

export const LoadingOverlay: React.FC<LoadingOverlayProps> = ({ 
  open, 
  message = 'Cargando...' 
}) => {
  return (
    <Fade in={open}>
      <Box
        sx={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(255, 255, 255, 0.8)',
          backdropFilter: 'blur(4px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 9999,
        }}
      >
        <LoadingSpinner size="large" message={message} variant="circular" />
      </Box>
    </Fade>
  );
};
