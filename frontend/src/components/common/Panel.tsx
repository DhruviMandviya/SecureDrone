import React from 'react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface PanelProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  headerRight?: React.ReactNode;
}

export const Panel: React.FC<PanelProps> = ({
  title,
  headerRight,
  className,
  children,
  ...props
}) => {
  return (
    <div
      className={cn(
        "bg-tactical-panel border border-tactical-border rounded-sm flex flex-col min-h-0 overflow-hidden relative",
        className
      )}
      {...props}
    >
      {/* Decorative corner markers */}
      <div className="absolute top-0 left-0 w-2 h-2 border-t border-l border-signal-cyan/30"></div>
      <div className="absolute top-0 right-0 w-2 h-2 border-t border-r border-signal-cyan/30"></div>
      <div className="absolute bottom-0 left-0 w-2 h-2 border-b border-l border-signal-cyan/30"></div>
      <div className="absolute bottom-0 right-0 w-2 h-2 border-b border-r border-signal-cyan/30"></div>

      {(title || headerRight) && (
        <div className="flex items-center justify-between px-3 py-1.5 border-b border-tactical-border/50 bg-[#121822] flex-shrink-0">
          {title && (
            <h2 className="text-[10px] font-sans font-bold uppercase tracking-widest text-[#a8b0ba] opacity-80">
              {title}
            </h2>
          )}

          {headerRight && (
            <div>
              {headerRight}
            </div>
          )}
        </div>
      )}

      <div className="p-3 flex-1 min-h-0">
        {children}
      </div>

    </div>
  );
};