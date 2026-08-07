import React, { useEffect, useState } from 'react';
import { Panel } from '../common/Panel';
import { DataReadout } from '../common/DataReadout';
import { usePolling } from '../../hooks/usePolling';
import { api } from '../../lib/api';
import { Lock, Unlock, RefreshCw } from 'lucide-react';

export const CryptoStatusPanel: React.FC = () => {
  const { data: sessions } = usePolling(api.getSessions, 7000);
  const activeSession = sessions?.find(s => s.active);

  const [rotations, setRotations] = useState(1);
  useEffect(() => {
    const timer = setInterval(() => setRotations(r => r + 1), 60000); // fake rotation every min
    return () => clearInterval(timer);
  }, []);

  return (
    <Panel title="ML-KEM Key Exchange" className="h-full">
      {activeSession ? (
        <div className="flex flex-col gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-signal-cyan/10 border border-signal-cyan rounded-full relative">
              <div className="absolute inset-0 rounded-full animate-ping bg-signal-cyan/20"></div>
              <Lock className="w-5 h-5 text-signal-cyan" />
            </div>
            <div>
              <div className="text-signal-cyan text-sm font-bold font-sans tracking-wide">SECURE HANDSHAKE OK</div>
              <div className="text-[10px] text-tactical-text mono">ID: {activeSession.session_id}</div>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-2 mt-2">
            <DataReadout label="ALGORITHM" value={activeSession.kem_algorithm} size="sm" color="text-white" />
            <DataReadout label="ROTATIONS" value={rotations.toString()} size="sm" color="text-white" />
            <DataReadout label="ESTABLISHED" value={new Date(activeSession.established_at).toLocaleTimeString()} size="sm" className="col-span-2" />
          </div>

          <div className="mt-auto border-t border-tactical-border pt-2 flex items-center justify-between text-xs text-tactical-text font-mono">
             <span>NEXT ROTATION IN:</span>
             <span className="text-alert-amber flex items-center gap-1"><RefreshCw className="w-3 h-3 animate-spin duration-[3000ms]" /> 00:59</span>
          </div>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center p-4 h-full text-center opacity-50 space-y-2">
          <Unlock className="w-8 h-8 text-alert-amber" />
          <span className="text-xs font-mono font-bold text-alert-amber">NO ACTIVE SESSION</span>
        </div>
      )}
    </Panel>
  );
};
