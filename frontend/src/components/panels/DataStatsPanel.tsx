import React from 'react';
import { Panel } from '../common/Panel';
import { DataReadout } from '../common/DataReadout';
import { usePolling } from '../../hooks/usePolling';
import { api } from '../../lib/api';
import { Activity } from 'lucide-react';

export const DataStatsPanel: React.FC = () => {
  const { data: sessions } = usePolling(api.getSessions, 2000);
  const activeSession = sessions?.find(s => s.active);

  const txBytes = activeSession?.bytes_sent || 0;
  const rxBytes = activeSession?.bytes_received || 0;
  const total = txBytes + rxBytes || 1; 
  const dropped = activeSession?.packets_dropped || 0;

  const txPercent = (txBytes / total) * 100;
  const rxPercent = (rxBytes / total) * 100;

  return (
    <Panel title="Network & Crypto Stats" className="h-[150px] lg:h-full flex-1">
       <div className="flex flex-col gap-4 h-full">
         
         <div className="flex flex-col gap-1">
            <div className="flex justify-between text-[9px] uppercase font-sans tracking-widest text-[#a8b0ba]">
               <span>TX (UPLINK)</span>
               <span className="text-white font-mono">{(txBytes / 1024).toFixed(1)} KB</span>
            </div>
            <div className="w-full h-1.5 bg-tactical-border overflow-hidden">
               <div className="h-full bg-signal-cyan" style={{ width: `${Math.max(5, txPercent)}%` }}></div>
            </div>
         </div>

         <div className="flex flex-col gap-1">
            <div className="flex justify-between text-[9px] uppercase font-sans tracking-widest text-[#a8b0ba]">
               <span>RX (DOWNLINK)</span>
               <span className="text-white font-mono">{(rxBytes / 1024).toFixed(1)} KB</span>
            </div>
            <div className="w-full h-1.5 bg-tactical-border overflow-hidden">
               <div className="h-full bg-signal-green" style={{ width: `${Math.max(5, rxPercent)}%` }}></div>
            </div>
         </div>

         <div className="mt-auto grid grid-cols-2 gap-2 pt-2 border-t border-tactical-border/50">
            <DataReadout label="DROPPED" value={dropped} size="sm" color={dropped > 5 ? 'text-alert-red' : 'text-signal-green'} />
            <div className="flex flex-col">
               <span className="text-[9px] uppercase tracking-widest text-[#a8b0ba]">SIGNAL</span>
               <Activity className="w-5 h-5 text-signal-cyan mt-1" />
            </div>
         </div>

       </div>
    </Panel>
  );
};
