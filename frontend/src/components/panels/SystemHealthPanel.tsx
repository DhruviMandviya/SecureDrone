import React from 'react';
import { Panel } from '../common/Panel';
import { LedIndicator } from '../common/LedIndicator';
import { usePolling } from '../../hooks/usePolling';
import { api } from '../../lib/api';
import { Server } from 'lucide-react';

export const SystemHealthPanel: React.FC = () => {
  const { data: status } = usePolling(api.getStatus, 3000);

 

  return (
  <Panel title="Ground Control Station" className="h-full flex flex-col gap-3">

    <div className="flex justify-between items-center bg-[#10151d] border border-tactical-border p-2 rounded-sm shadow-inner">
      <div className="flex items-center gap-2">
        <Server className="w-4 h-4 text-tactical-text" />
        <span className="text-xs font-sans tracking-wide text-white">
          STATUS
        </span>
      </div>

      <LedIndicator
        status={status?.ground_station === "Running" ? "nominal" : "warning"}
        label={status?.ground_station ?? "--"}
      />
    </div>

    <div className="grid grid-cols-2 gap-2 mt-2">

      <div className="border border-tactical-border/40 p-2">
        <span className="text-[9px] uppercase tracking-widest text-[#a8b0ba]">
          Active Sessions
        </span>

        <div className="text-lg font-mono text-signal-cyan">
          {status?.active_sessions ?? "--"}
        </div>
      </div>

      <div className="border border-tactical-border/40 p-2">
        <span className="text-[9px] uppercase tracking-widest text-[#a8b0ba]">
          Telemetry Packets
        </span>

        <div className="text-lg font-mono text-signal-cyan">
          {status?.telemetry_packets ?? "--"}
        </div>
      </div>

    </div>

    <div className="mt-2 border border-tactical-border/40 p-2">

      <span className="text-[9px] uppercase tracking-widest text-[#a8b0ba]">
        Latest Telemetry
      </span>

      <LedIndicator
        status={status?.latest_available ? "nominal" : "warning"}
        label={status?.latest_available ? "AVAILABLE" : "NOT AVAILABLE"}
      />

    </div>

  </Panel>
  );
};