import React from 'react';
import { Fade, Slide, Zoom, Grow, Collapse } from '@mui/material';
import { TransitionProps } from '@mui/material/transitions';

// Transición de fade in desde arriba
export const SlideDownTransition = React.forwardRef<
  unknown,
  TransitionProps & { children: React.ReactElement }
>((props, ref) => (
  <Slide direction="down" ref={ref} {...props} />
));

// Transición de fade in desde la izquierda
export const SlideRightTransition = React.forwardRef<
  unknown,
  TransitionProps & { children: React.ReactElement }
>((props, ref) => (
  <Slide direction="right" ref={ref} {...props} />
));

// Transición de zoom in
export const ZoomTransition = React.forwardRef<
  unknown,
  TransitionProps & { children: React.ReactElement }
>((props, ref) => (
  <Zoom ref={ref} {...props} />
));

// Transición de grow
export const GrowTransition = React.forwardRef<
  unknown,
  TransitionProps & { children: React.ReactElement }
>((props, ref) => (
  <Grow ref={ref} {...props} />
));

// Transición de fade
export const FadeTransition = React.forwardRef<
  unknown,
  TransitionProps & { children: React.ReactElement }
>((props, ref) => (
  <Fade ref={ref} {...props} />
));

// Transición de collapse
export const CollapseTransition = React.forwardRef<
  unknown,
  TransitionProps & { children: React.ReactElement }
>((props, ref) => (
  <Collapse ref={ref} {...props} />
));

// Component wrapper para staggered animations
interface StaggeredChildrenProps {
  children: React.ReactNode[];
  delay?: number;
}

export const StaggeredChildren: React.FC<StaggeredChildrenProps> = ({ 
  children, 
  delay = 100 
}) => {
  return (
    <>
      {React.Children.map(children, (child, index) => (
        <Fade
          in={true}
          timeout={600}
          style={{ transitionDelay: `${index * delay}ms` }}
        >
          <div>{child}</div>
        </Fade>
      ))}
    </>
  );
};
