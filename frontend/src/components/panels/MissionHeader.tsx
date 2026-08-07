import React, { useState, useEffect } from 'react';
import { Shield, Activity } from 'lucide-react';
import { LedIndicator } from '../common/LedIndicator';
import { api } from '../../lib/api';
import { usePolling } from '../../hooks/usePolling';

export const MissionHeader: React.FC = () => {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const { data: status } = usePolling(api.getStatus, 5000);

  const formatTime = (date: Date) => {

  return date.toLocaleString("en-IN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  });

};

  const getSystemLed = () => {
    if (!status) return 'off';

    if (status.active_sessions > 0)
      return 'nominal';

    return 'warning';
  };

  return (
    <header className="col-span-full h-14 bg-tactical-panel border-b border-tactical-border flex items-center justify-between px-4 sticky top-0 z-40 relative">

      <div className="absolute inset-0 bg-scanlines opacity-20 pointer-events-none"></div>

      <div className="flex items-center gap-4 z-10">
        <div className="flex flex-col">
          <h1 className="text-sm font-sans font-bold flex items-center gap-2 text-white uppercase tracking-widest">
            <Shield className="w-4 h-4 text-signal-cyan" />
            SecureDrone GCS
          </h1>

          <span className="text-[10px] text-signal-cyan font-mono tracking-widest">
            ML-KEM / AES-256
          </span>
        </div>
      </div>

      <div className="flex items-center gap-8 hidden md:flex">

        <LedIndicator
          status={getSystemLed()}
          label="UPLINK"
          blink={status?.active_sessions! > 0}
        />

        <LedIndicator
          status={status?.active_sessions! > 0 ? 'nominal' : 'warning'}
          label="CRYPTO"
        />

        <div className="flex items-center gap-2 border-l border-tactical-border pl-8">
          <Activity className="w-3 h-3 text-tactical-text opacity-70" />

          <span className="text-xs font-mono font-bold text-white">
            SYS HLT: {status?.ground_station || "WAIT"}
          </span>

        </div>

      </div>

      <div className="flex flex-col items-end">
        <span className="text-white font-mono font-bold text-sm">
          {formatTime(time)}IST
        </span>

        <span className="text-[10px] text-tactical-text uppercase tracking-widest">
          Mission Elapsed Time
        </span>
      </div>

    </header>
  );
};