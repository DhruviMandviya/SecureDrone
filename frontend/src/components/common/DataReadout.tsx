import React from 'react';
import { cn } from './Panel';

interface DataReadoutProps {
  label: string;
  value: string | number;
  unit?: string;
  size?: 'sm' | 'md' | 'lg';
  mono?: boolean;
  color?: string;
  className?: string;
}

export const DataReadout: React.FC<DataReadoutProps> = ({ 
  label, 
  value, 
  unit, 
  size = 'md', 
  mono = true,
  color = 'text-white',
  className
}) => {
  const sizeClasses = {
    sm: 'text-xs',
    md: 'text-lg',
    lg: 'text-2xl'
  };

  return (
    <div className={cn("flex flex-col", className)}>
      <span className="font-sans text-[9px] uppercase tracking-widest text-[#a8b0ba] opacity-70 mb-0.5">
        {label}
      </span>
      <div className="flex items-baseline gap-1">
        <span className={cn(
          "font-bold font-mono tracking-tight", 
          sizeClasses[size], 
          color,
          !mono && 'font-sans'
        )}>
          {value}
        </span>
        {unit && (
          <span className="font-sans text-[10px] text-tactical-text ml-0.5 font-semibold">
            {unit}
          </span>
        )}
      </div>
    </div>
  );
};
