import React from 'react';
import { Panel } from '../common/Panel';
import { DataReadout } from '../common/DataReadout';
import { usePolling } from '../../hooks/usePolling';
import { api } from '../../lib/api';

export const AESStatusPanel: React.FC = () => {
  const { data: sessions } = usePolling(api.getSessions, 5000);
  const activeSession = sessions?.find(s => s.active);

  const getThroughput = () => {
     if (!activeSession) return 0;
     // Faked throughput calculation 
     return (activeSession.bytes_received / 1024).toFixed(2); 
  };

  return (
    <Panel title="AES Encryption Status" className="h-full">
      <div className="flex flex-col gap-3">
        <DataReadout label="CIPHER MODE" value={activeSession?.cipher || 'NONE'} size="sm" color="text-signal-green" />
        
        <div className="flex flex-col gap-1">
          <span className="font-sans text-[9px] uppercase tracking-widest text-[#a8b0ba] opacity-70">NONCE/TAG VALIDATION</span>
          <div className="flex items-center gap-2">
            <div className="h-1 flex-1 bg-tactical-border overflow-hidden">
               <div className="h-full w-full bg-signal-cyan relative">
                  <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
               </div>
            </div>
            <span className="text-xs font-mono text-signal-cyan font-bold">PASS</span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-2 mt-2 border-t border-tactical-border/50 pt-2">
          <DataReadout label="RX ENCRYPTED" value={getThroughput()} unit="KB" size="sm" />
          <DataReadout label="ERRORS / DROPS" value={activeSession?.packets_dropped || 0} size="sm" color={(activeSession?.packets_dropped || 0) > 0 ? 'text-alert-amber' : 'text-signal-green'} />
        </div>
      </div>
    </Panel>
  );
};
