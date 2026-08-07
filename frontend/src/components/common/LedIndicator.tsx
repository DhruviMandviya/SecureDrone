import React from 'react';
import { cn } from './Panel';

export type LedStatus = 'nominal' | 'warning' | 'critical' | 'off' | 'active';

interface LedIndicatorProps {
  status: LedStatus;
  label?: string;
  blink?: boolean;
}

export const LedIndicator: React.FC<LedIndicatorProps> = ({ status, label, blink }) => {
  
  const getColors = (status: LedStatus) => {
    switch (status) {
      case 'nominal':
        return 'bg-signal-green shadow-[0_0_8px_rgba(0,255,65,0.7)]';
      case 'warning':
        return 'bg-alert-amber shadow-[0_0_8px_rgba(255,176,0,0.7)]';
      case 'critical':
        return 'bg-alert-red shadow-[0_0_8px_rgba(255,42,42,0.7)]';
      case 'active':
        return 'bg-signal-cyan shadow-[0_0_8px_rgba(0,240,255,0.7)]';
      case 'off':
      default:
        return 'bg-tactical-border shadow-none';
    }
  };

  return (
    <div className="flex items-center gap-2">
      <div className={cn(
        "w-2.5 h-2.5 rounded-sm border border-black/50 transition-colors duration-300",
        getColors(status),
        blink && status !== 'off' ? 'animate-pulse' : ''
      )} />
      {label && <span className="font-sans text-[10px] uppercase tracking-wider text-tactical-text">{label}</span>}
    </div>
  );
};
