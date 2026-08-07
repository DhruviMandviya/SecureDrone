import React from 'react';
import { Panel } from '../common/Panel';
import { LedIndicator } from '../common/LedIndicator';
import { usePolling } from '../../hooks/usePolling';
import { api } from '../../lib/api';
import { Wifi, AlertTriangle } from 'lucide-react';

export const DroneStatusPanel: React.FC = () => {
  const { data: telemetry } = usePolling(api.getTelemetryLatest, 1000);
  const { data: status } = usePolling(api.getStatus, 5000);

  return (
    <Panel title="Drone Link Status" className="h-full border-t-[2px] border-t-alert-amber">
      
      <div className="flex items-center gap-4 border-b border-tactical-border/50 pb-3 mb-3">
        <Wifi className="w-6 h-6 text-signal-cyan animate-pulse" />
        <div className="w-full flex flex-col gap-1">
          <div className="flex justify-between text-[10px] font-sans tracking-widest">
            <span>LINK QUALITY</span>
            <span className="text-signal-cyan">{status?.link_quality}%</span>
          </div>
          <div className="w-full h-1.5 bg-tactical-border rounded-sm overflow-hidden">
            <div 
              className="h-full bg-signal-cyan" 
              style={{ width: `${status?.link_quality || 0}%` }}
            ></div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-3">
         <LedIndicator status={telemetry?.armed ? 'critical' : 'warning'}  // Need precise LedStatus, using 'critical'/'warning'
                       label={telemetry?.armed ? 'ARMED' : 'DISARMED'} />
         <LedIndicator status={status?.drone_connection === 'connected' ? 'nominal' : 'critical'} 
                       label={status?.drone_connection === 'connected' ? 'CONNECTED' : 'DSCHD'} />
      </div>

      <div className="flex flex-col flex-1">
         <div className="text-[10px] text-tactical-text mb-1 uppercase tracking-widest">Active Alarms</div>
         <div className="flex-1 bg-black/40 border border-[#ff2a2a]/20 p-2 overflow-y-auto">
            {status?.active_alarms && status.active_alarms.length > 0 ? (
               <ul className="space-y-1">
                  {status.active_alarms.map((a, i) => (
                     <li key={i} className="text-[10px] font-mono text-alert-red flex items-center gap-1">
                        <AlertTriangle className="w-3 h-3" /> {a}
                     </li>
                  ))}
               </ul>
            ) : (
               <span className="text-[10px] font-mono text-signal-green opacity-70">NO ACTIVE ALARMS</span>
            )}
         </div>
      </div>

    </Panel>
  );
};
