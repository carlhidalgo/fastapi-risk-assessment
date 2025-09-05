import React from 'react';
import { Card, CardContent, CardActions, IconButton, Tooltip } from '@mui/material';
import { motion } from 'framer-motion';
import { styled } from '@mui/material/styles';

const AnimatedCard = styled(motion.div)(({ theme }) => ({
  width: '100%',
  height: '100%',
  cursor: 'pointer',
  '& .MuiCard-root': {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    position: 'relative',
    overflow: 'hidden',
    background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
    '&::before': {
      content: '""',
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      height: '4px',
      background: `linear-gradient(90deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
      transform: 'scaleX(0)',
      transformOrigin: 'left',
      transition: 'transform 0.3s ease'
    },
    '&:hover::before': {
      transform: 'scaleX(1)'
    }
  }
}));

interface EnhancedCardProps {
  children: React.ReactNode;
  onClick?: () => void;
  delay?: number;
  actions?: React.ReactNode;
}

export const EnhancedCard: React.FC<EnhancedCardProps> = ({ 
  children, 
  onClick, 
  delay = 0,
  actions 
}) => {
  return (
    <AnimatedCard
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.4, ease: [0.6, -0.05, 0.01, 0.99] }}
      whileHover={{ 
        y: -8,
        transition: { type: "spring", stiffness: 300, damping: 20 }
      }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
    >
      <Card elevation={2}>
        <CardContent sx={{ flexGrow: 1 }}>
          {children}
        </CardContent>
        {actions && (
          <CardActions sx={{ justifyContent: 'flex-end', p: 2 }}>
            {actions}
          </CardActions>
        )}
      </Card>
    </AnimatedCard>
  );
};

// Botón con animación mejorada
export const AnimatedIconButton: React.FC<{
  children: React.ReactNode;
  onClick?: () => void;
  tooltip?: string;
  color?: 'primary' | 'secondary' | 'default' | 'error' | 'warning' | 'info' | 'success';
}> = ({ children, onClick, tooltip, color = 'default' }) => {
  const button = (
    <motion.div
      whileHover={{ 
        scale: 1.1, 
        rotate: 5,
        transition: { type: "spring", stiffness: 300, damping: 20 }
      }}
      whileTap={{ scale: 0.9 }}
    >
      <IconButton onClick={onClick} color={color} size="small">
        {children}
      </IconButton>
    </motion.div>
  );

  return tooltip ? (
    <Tooltip title={tooltip} arrow>
      {button}
    </Tooltip>
  ) : button;
};

// Chip animado para estados
export const StatusChip: React.FC<{
  label: string;
  color: 'primary' | 'secondary' | 'success' | 'error' | 'warning' | 'info';
  delay?: number;
}> = ({ label, color, delay = 0 }) => {
  const getColor = (color: string) => {
    const colors = {
      primary: '#2563eb',
      secondary: '#10b981',
      success: '#10b981',
      error: '#ef4444',
      warning: '#f59e0b',
      info: '#06b6d4'
    };
    return colors[color as keyof typeof colors] || colors.primary;
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ 
        delay, 
        type: "spring", 
        stiffness: 500, 
        damping: 20 
      }}
      whileHover={{ scale: 1.05 }}
      style={{
        display: 'inline-block',
        padding: '4px 12px',
        borderRadius: '16px',
        backgroundColor: getColor(color),
        color: 'white',
        fontSize: '0.75rem',
        fontWeight: 500,
        textTransform: 'uppercase',
        letterSpacing: '0.5px'
      }}
    >
      {label}
    </motion.div>
  );
};
